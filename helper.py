
import pandas as pd
import re

def extract_chinese_characters(text: str):
    # Regular expression pattern to match Chinese characters
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    chinese_characters = chinese_pattern.findall(text)
    chinese_characters = list(''.join(chinese_characters))
    return list(dict.fromkeys(chinese_characters))

def filter_dataframe_by_character(df, character_tuple, column_name='character'):
    # Convert the tuple to a DataFrame with a temporary index column
    temp_df = pd.DataFrame({column_name: character_tuple})
    temp_df['temp_index'] = range(len(temp_df))
    
    # Merge the DataFrame on the specified column to filter rows
    merged_df = df.merge(temp_df, on=column_name)
    
    # Sort the DataFrame based on the temporary index to restore the original order
    filtered_df = merged_df.sort_values('temp_index').drop(columns='temp_index')
    
    return filtered_df

def remove_characters(text: str, characters_to_remove):
    # Create a translation table that maps each character in 'characters_to_remove' to None
    translation_table = str.maketrans('', '', ''.join(characters_to_remove))
    
    # Use the translation table to remove the characters from the text
    cleaned_text = text.translate(translation_table)
    
    return cleaned_text

# Example usage:
# Assuming dfMain is your main DataFrame with 'd_radical' column and dfSub is the DataFrame with 't_radical' column
# merged_df = lookup_and_copy_values(dfMain, dfSub)

import pandas as pd

def lookup_and_copy_values(dfMain, dfMainColumn,dfSub,dfSubColumn):
    # Create an empty dictionary to store the matching values from dfSub
    match_dict = {}
    
    # Loop through the rows in dfMain and check for partial matches in dfSub
    for index, row in dfMain.iterrows():
        d_radical = row[dfMainColumn]
        matching_rows = dfSub[dfSub[dfSubColumn].str.contains(d_radical, na=False)]
        
        # Check if there are any partial matches in dfSub
        if not matching_rows.empty:
            # Store the first match in the dictionary
            match_dict[index] = matching_rows.iloc[0].to_dict()
    
    # Convert the dictionary to a DataFrame with the same index as dfMain
    matched_values_df = pd.DataFrame.from_dict(match_dict, orient='index')
    
    # Merge dfMain with matched_values_df to update the values
    merged_df = dfMain.merge(matched_values_df, left_index=True, right_index=True, how='left')
    
    # Drop the 't_radical' column from the merged DataFrame
    # merged_df.drop(columns=[dfSubColumn], inplace=True)
    
    return merged_df

# Example usage:
# Assuming dfMain is your main DataFrame with 'd_radical' column and dfSub is the DataFrame with 't_radical' column
# merged_df = lookup_and_copy_values(dfMain, dfSub)
