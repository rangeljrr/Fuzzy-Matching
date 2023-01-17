# Import dependencies
import pandas as pd

from fuzzywuzzy import fuzz
from os import listdir
from os.path import isfile, join

from _config import fuzzy_target, input_path,results_path, source_path
from _preprocess_functions import create_columns, create_target, preprocess_series

def score_strings(string1, string2):
    """ This function will take two strings as inputs and find the 
        ratio, partial_ratio, and token_sort_ratio scores. The scores will
        then be ensembled to create 1 final score """
    
    # Computing the ratio, partial ratio, and token sort ratio scores
    ratio_score = fuzz.ratio(string1, string2)
    partial_ratio_score = fuzz.partial_ratio(string1, string2)
    token_sort_ratio_score = fuzz.token_sort_ratio(string1, string2)
    
    # Ensembling the scores to create 1 single output
    ensembled_score = int((ratio_score + partial_ratio_score + token_sort_ratio_score) / 3)
    
    return ensembled_score

def token_intersection(str1, str2):
    """ This function will take two strings, split the strings into tokens, 
        and find the lenth of common tokens """
    
    str1 = set(str1.split())
    str2 = set(str2.split())
    
    
    return len(str1.intersection(str2))

def list_files(path):
    """ This function will take an input path and return a list of all files in
        the directory """
    
    list_of_files = [f for f in listdir(path) if isfile(join(path, f))]
    
    return list_of_files

    

def roddys_fuzzy_main(input_file_path, source_file_path,write_results_path, use_token_reduction=True):
    
    """ This function takes the source, input files and runs the fuzzy logic. It then saves the results to the specified directory"""
    
    # Reading in files
    input_data = pd.read_csv(input_file_path)
    source_data = pd.read_csv(source_file_path)
    
    # Clean up the input data
    #input_data = create_target(input_data)

    # Clean up the source data
    #source_data = create_target(source_data)

    # Initializing Dataframe
    results = pd.DataFrame()

    # First Narrow down the fields using a common score (intersection)
    for i in range(input_data.shape[0]):
        
        target = input_data.iloc[i][fuzzy_target]

        # Use token reduction
        if use_token_reduction == True:
            fuzzy_dataframe = source_data.copy()
            fuzzy_dataframe['score'] = fuzzy_dataframe[fuzzy_target].apply(lambda x: token_intersection(x,target))# <-- Will need to rename and redo this algorithm
            most_common = max(fuzzy_dataframe['score'])
            fuzzy_dataframe = fuzzy_dataframe[fuzzy_dataframe['score'] == most_common]
        
        # Do not use token reduction
        else:
            fuzzy_dataframe = source_data.copy()
            
        # Need to create the distance array from the dictionary
        fuzzy_dataframe['score'] = fuzzy_dataframe[fuzzy_target].apply(lambda x: score_strings(x,target))
        max_score = max(fuzzy_dataframe['score'])
        best_match = fuzzy_dataframe[fuzzy_dataframe['score'] == max_score].iloc[0]
        
        # Finally neeed to append to master dataframe
        input_row = input_data.iloc[[i]]
        del input_row[fuzzy_target]
        
        match_row = source_data[source_data[fuzzy_target] == best_match[fuzzy_target]]
        del match_row[fuzzy_target]
        
        append_to_results = pd.concat([input_row, match_row], axis=1)
        append_to_results['Score'] = best_match['score']
        results = results.append(append_to_results)
        
    rename_columns = create_columns()
    
    results.columns = rename_columns
    
    #del results['Target']
    
    results.to_csv(write_results_path, index=False)