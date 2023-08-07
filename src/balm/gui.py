'''
Created on Aug 6, 2023

@author: immanueltrummer
'''
from io import StringIO
from langchain import PromptTemplate
from langchain.llms import OpenAI

import pandas as pd
import streamlit as st


st.set_page_config(page_title='BALM')
st.header('BALM: Batch Analysis with Language Models')

in_files = st.file_uploader(
    'Input files:', accept_multiple_files=True, type=['txt'])

task = st.text_area('Prompt (task description):')
ai_key = st.text_input('OpenAI key', type='password')

template = PromptTemplate.from_template('{input_text}\n' + task + '\n')
llm = OpenAI(model_name='text-davinci-002', openai_api_key=ai_key)

if st.button('Process Data'):
    results = []
    for in_file in in_files:
        
        file_name = in_file.name
        in_text = StringIO(in_file.getvalue().decode('utf-8')).read()
        prompt = template.format(input_text=in_text)
        answer = llm(prompt)
        results += [[file_name, answer]]
        
        result_row = pd.DataFrame({'filename':[file_name], 'answer':[answer]})
        if 'result_display' not in globals():
            result_display = st.dataframe(result_row, use_container_width=True)
        else:
            result_display.add_rows(result_row)

    
    results_df = pd.DataFrame(results, columns=['filename', 'answer'])
    results_csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        'Download Results', results_csv, 'results.csv', 'text/csv')