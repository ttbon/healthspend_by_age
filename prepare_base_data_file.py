import numpy as np
import pandas as pd
import os

"""
When run, this file outputs the filtered, cleaned MEPS dataset we use to inform the spending
for eachindividual user and insurance plan combination. The file takes the raw MEPS
consolidated household file and a reference csv file that simplifies processing and filtering
"""

def import_meps_data(meps_data_loc):
    """
    function imports the raw meps data
    params: meps data file location in .dta format
    return: pandas dataframe of the imported data
    """
    meps_df = pd.read_stata(meps_data_loc)
    meps_df.columns = meps_df.columns.str.lower()
    return meps_df

def import_lookup(lookup_loc):
    """
    function imports the lookup csv
    params: lookup csv file location
    return: pandas dataframe
    """
    lookup_df = pd.read_csv(lookup_loc)
    return lookup_df

def extract_array(lookup_df, var):
    """
    generic function that parses specific rows of the lookup_df
    params: lookup dataframe, variable from lookup dataframe that needs to be extracted
    return: numpy array of parsed values
    """
    var_vals = np.empty(0)
    idx = lookup_df.loc[lookup_df['variable'] == var]['value'].index[0]
    var_vals = np.append(var_vals, lookup_df.loc[lookup_df['variable'] == var]['value'][idx].split(","))
    return var_vals

def gen_array_of_cols_needed(lookup_df):
    """
    generates a numpy array of all columns we'd like to keep
    params: lookup dataframe
    return: numpy array of needed columns
    """
    col_list = np.empty(0)
    for var in ['id_variable_list', 'cohort_variable_list', 'other_variable_list', 'all_health_expense_var_list',
                'all_health_expense_count_list']:
        col_list = np.append(col_list, extract_array(lookup_df, var))
    col_list = col_list.astype(str)
    return col_list

def return_subset_cols(meps_df, needed_cols):
    """
    returns a subset dataframe
    params: meps dataframe, numpy array of needed columns
    return: meps dataframe with subset of columns
    """
    return meps_df[needed_cols]

def rename_columns(lookup_df, meps_df):
    """
    returns the meps dataframe with columns renamed
    params: lookup dataframe, meps dataframe
    return: meps dataframe with columns renamed
    """
    rename_cols = np.empty(0)
    for var in ['id_variable_rename_list', 'cohort_variable_rename_list', 'other_variable_rename_list',
                'all_health_expense_var_rename_list', 'all_health_expense_count_rename_list']:
        rename_cols = np.append(rename_cols, extract_array(lookup_df, var))
    rename_cols = rename_cols.astype(str)
    meps_df.columns = rename_cols
    return meps_df

def clean_str_values(lookup_df, meps_df):
    """
    returns the meps dataframe with some variable values processed
    params: lookup dataframe, meps dataframe
    return: meps dataframe with certain variable values having " " replaced with "_"
    """
    string_cols = np.empty(0)
    for var in ['string_variable_list']:
        string_cols = np.append(string_cols, extract_array(lookup_df, var))
    for col in string_cols:
        meps_df[col] = meps_df[col].str.replace(" ", "_")
    return meps_df

def filter_observations(lookup_df, meps_df):
    """
    filters the meps dataframe with observations not needed as specified in lookup dataframe
    params: lookup dataframe, meps dataframe
    return: filtered meps dataframe
    """
    all_vars = np.empty(0)
    for var in ['all_filter_variable_list']:
        all_vars = np.append(all_vars, extract_array(lookup_df, var))

    all_vars_vals = np.empty(0)
    for var in ['all_filter_variable_val_list']:
        all_vars_vals = np.append(all_vars_vals, extract_array(lookup_df, var))

    all_vars_vals_types = np.empty(0)
    for var in ['all_filter_variable_type_list']:
        all_vars_vals_types = np.append(all_vars_vals_types, extract_array(lookup_df, var))

    for i in range(0, all_vars.shape[0]):
        var_vals = extract_array(lookup_df, all_vars_vals[i])
        if all_vars_vals_types[i] == 'string':
            var_vals = var_vals.astype(str)
        elif all_vars_vals_types[i] == 'integer':
            var_vals = var_vals.astype(int)
        else:
            raise Exception("Unhandled type")

        meps_df = meps_df.loc[~meps_df[all_vars[i]].isin(var_vals)]

    meps_df.reset_index(drop=True, inplace=True)
    return meps_df

def main(meps_data_loc="data/full2019_expenses.dta",
         lookup_loc="base_data_lookup.csv",
         outpath="data/base_meps_data.csv"):

    """
    wrapper function to run the process
    params: meps data location, lookup data location, outpath location
    return: meps dataframe with added column for age_band
    """

    meps_df = import_meps_data(meps_data_loc)
    lookup_df = import_lookup(lookup_loc)
    col_list = gen_array_of_cols_needed(lookup_df)
    meps_df = return_subset_cols(meps_df, col_list)
    meps_df = rename_columns(lookup_df, meps_df)
    meps_df = clean_str_values(lookup_df, meps_df)
    meps_df = filter_observations(lookup_df, meps_df)
    meps_df.to_csv(outpath, index=False)
    return

if __name__ == '__main__':
    main()
