from _config import fuzzy_target
def preprocess_series(series, lowercase=True, remove_special=True, remove_numbers=True):
    """ This function pre-processes a string with the conditions below 
        - Remove special characters
        - Lowercase """
    
    # Lowercase
    if lowercase == True:
        series = series.str.lower()
    
    # Remove special characters
    if remove_special == True:
        series = series.str.replace('[^\w\s]','')
    
    # Remove numbers
    if remove_numbers == True:
        series = series.str.replace('\d+','')
        
    return series

def create_target(dataframe, path):
    """ This function will create the fuzzy matching target and save the data as a .csv"""
    
    dataframe[fuzzy_target] = preprocess_series(dataframe['First Name'], lowercase=True, remove_special=True, remove_numbers=True) + ' ' + \
                           preprocess_series(dataframe['Last Name'], lowercase=True, remove_special=True, remove_numbers=True) + ' ' + \
                           preprocess_series(dataframe['Street Address'], lowercase=True, remove_special=True, remove_numbers=False)
    
    dataframe.to_csv(path, index=False)
    
def delete_target(dataframe, path):
    """ This function will delete the fuzzy matching target and save the data as a .csv"""
    
    del dataframe[fuzzy_target]
    dataframe.to_csv(path, index=False) 



def create_columns():
    return ['First Name', 'Last Name', 'Street Address',
            'Match First Name','Match Last Name','Match Street Address','Confidence Score']