'''
Created on Aug 7, 2023

@author: immanueltrummer
'''
import altair as alt
import pandas as pd
import streamlit as st


class Analysis():
    """ Analyzes BALM results for visualizations. """
    
    def __init__(self, results, selected_models):
        """ Initialize with models and results.
        
        Args:
            results: list of rows (as dictionaries).
            selected_models: list of model labels.
        """
        self.results = results
        self.results_df = pd.DataFrame(results)
        self.selected_models = selected_models
    
    def add_value_stats(self):
        """ Add value distribution for each column. """
        with st.expander('Output Distribution'):
            for model_label in self.selected_models:
                model_results = self.results_df[model_label]
                histogram = model_results.value_counts().reset_index()
                histogram.columns = ['Output', 'Count']
                chart = alt.Chart(histogram).mark_bar().encode(
                    x='Output', y='Count').properties(title=model_label)
                st.altair_chart(chart, use_container_width=False)
    
    def add_overlap_info(self):
        """ Add visualizations on overlap between different models. """
        with st.expander('Model Agreement'):
            nr_results = len(self.results)
            ratio_table = []
            for model_1 in self.selected_models:
                ratio_row = {}
                ratio_row['Compared Model'] = model_1
                for model_2 in self.selected_models:
                    overlap = self.results_df[model_1] == self.results_df[model_2]
                    nr_same = sum(overlap)
                    ratio = nr_same / nr_results
                    ratio_row[model_2] = ratio
                
                ratio_table.append(ratio_row)
            st.dataframe(ratio_table)