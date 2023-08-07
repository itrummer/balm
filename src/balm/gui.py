'''
Created on Aug 6, 2023

@author: immanueltrummer
'''
import os
import pathlib
import pandas as pd
import streamlit as st
import sys

cur_file_dir = os.path.dirname(__file__)
root_dir = pathlib.Path(cur_file_dir).parent.parent
sys.path.append(str(root_dir))

import balm.models

st.set_page_config(page_title='BALM')
st.header('BALM: Batch Analysis with Language Models')

with st.expander('API Credentials'):
    st.write('Enter API access keys for one or multiple model providers.')
    openai_key = st.text_input('OpenAI key:', type='password')
    #huggingface_key = st.text_input('Hugging Face Hub key:', type='password')
    credentials = {
        'OpenAI':openai_key, 
        #'Hugging Face Hub':huggingface_key
        }

models = balm.models.Models(root_dir, credentials)
available_models = models.available_models()
if not available_models:
    st.warning('Enter API Credentials to unlock models.')
model_name = st.selectbox('Model:', available_models)
task = st.text_area('Prompt (task description):')

with st.form('submission-form', clear_on_submit=True):
    upload_args = {'accept_multiple_files':True, 'type':['txt']}
    in_files = st.file_uploader('Input files:', **upload_args)
    submitted = st.form_submit_button('Process Data')

if submitted and in_files:
    results = []
    result_display = None
    for in_file in in_files:
        file_name = in_file.name
        answer = models.apply_model(model_name, in_file, task)
        results += [[file_name, answer]]
        
        result_row = pd.DataFrame({'filename':[file_name], 'answer':[answer]})
        if result_display is None:
            result_display = st.dataframe(result_row, use_container_width=True)
        else:
            result_display.add_rows(result_row)

    results_df = pd.DataFrame(results, columns=['filename', 'answer'])
    results_csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        'Download Results', results_csv, 'results.csv', 'text/csv')