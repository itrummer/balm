'''
Created on Aug 8, 2023

@author: immanueltrummer
'''
import io
import pandas as pd
import streamlit as st


def load_from_csv():
    """ Displays controls for uploading .csv files.
    
    Returns:
        list of input strings.
    """
    limit_rows = st.checkbox('Limit rows', value=False)
    max_rows = 0
    if limit_rows:
        st.write('Limiting number of rows')
        max_rows = st.number_input(
            'Maximal number of rows:', min_value=1, 
            value=10, max_value=1000)

    with st.form('submission-form', clear_on_submit=True):
        upload_args = {'accept_multiple_files':False, 'type':['csv']}
        csv_file = st.file_uploader('Input files:', **upload_args)        

        column_idx = st.number_input(
            'Index of input column (starting with 0):', 
            min_value=0, max_value=1000)
        
        submitted = st.form_submit_button('Process Data')
        
    if submitted:
        df = pd.read_csv(csv_file)
        nr_columns = len(df.columns)
        if column_idx >= nr_columns:
            st.error(f'Input file has only {nr_columns} columns!')
            return []

        input_column = df.iloc[:, column_idx]
        if max_rows:
            input_column = input_column[:max_rows]
        return list(input_column)
    
    else:
        return []


def load_from_text():
    """ Load input from text files. 
    
    Returns:
        list of input text documents as strings.
    """
    with st.form('submission-form', clear_on_submit=True):
        upload_args = {'accept_multiple_files':True, 'type':['txt']}
        in_files = st.file_uploader('Input files:', **upload_args)
        submitted = st.form_submit_button('Process Data')
    
    if submitted:
        inputs = []
        for in_file in in_files:
            text = io.StringIO(in_file.getvalue().decode('utf-8')).read()
            inputs += [text]
    
        return inputs
    else:
        return []