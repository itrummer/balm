'''
Created on Aug 6, 2023

@author: immanueltrummer
'''
import io
import os
import pathlib
import pandas as pd
import streamlit as st
import sys

cur_file_dir = os.path.dirname(__file__)
root_dir = pathlib.Path(cur_file_dir).parent.parent
sys.path.append(str(root_dir))

import balm.analysis
import balm.models
import balm.prompt

st.set_page_config(page_title='BALM')
st.header('BALM: Batch Analysis with Language Models')

with st.expander('Credentials'):
    st.write('Enter API access keys for one or multiple model providers.')
    openai_key = st.text_input('OpenAI key:', type='password')
    #huggingface_key = st.text_input('Hugging Face Hub key:', type='password')
    credentials = {
        'OpenAI':openai_key, 
        #'Hugging Face Hub':huggingface_key
        }

with st.expander('Models'):
    models = balm.models.Models(root_dir, credentials)
    available_models = models.available_models()
    if not available_models:
        st.warning('Enter API Credentials to unlock models.')
    nr_models = st.number_input(
        'Number of models:', value=1, min_value=1, max_value=5)
    selected_models = []
    for i in range(1, nr_models+1):
        select_label = f'Model {i}:'
        model_label = st.selectbox(select_label, available_models)
        selected_models.append(model_label)

task = st.text_area('Prompt (task description):')
with st.expander('Examples'):
    st.write('Include examples to improve model performance.')
    nr_examples = st.number_input(
        'Number of examples:', value=0, min_value=0, max_value=5)
    examples = []
    for i in range(1, nr_examples+1):
        example_label = f'Example {i}:'
        example_input = st.text_input('Example input:', key=f'ExampleIn{i}')
        example_output = st.text_input('Example output:', key=f'ExampleOut{i}')
        examples.append((example_input, example_output))

with st.form('submission-form', clear_on_submit=True):
    upload_args = {'accept_multiple_files':True, 'type':['txt']}
    in_files = st.file_uploader('Input files:', **upload_args)
    submitted = st.form_submit_button('Process Data')

if submitted and in_files:
    prompts = balm.prompt.PromptGenerator(task, examples)
    results = []
    result_display = None
    for in_file in in_files:
        text = io.StringIO(in_file.getvalue().decode('utf-8')).read()
        prompt = prompts.prompt(text)
        file_name = in_file.name
        model2answer = {}
        for model_label in selected_models:
            answer = models.apply_model(model_label, prompt)
            model2answer[model_label] = answer

        result = {'filename':file_name, 'prompt':prompt} | model2answer
        results.append(result)
        result_df = pd.DataFrame([result])
        if result_display is None:
            result_display = st.dataframe(result_df, use_container_width=True)
        else:
            result_display.add_rows(result_df)

    results_df = pd.DataFrame(results)
    results_csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        'Download Results', results_csv, 'results.csv', 'text/csv')
    
    st.header('Result Analysis')
    analysis = balm.analysis.Analysis(results, selected_models)
    analysis.add_value_stats()
    analysis.add_overlap_info()