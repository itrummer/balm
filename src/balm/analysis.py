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
        for model_label in self.selected_models:
            model_results = self.results_df[model_label]
            st.write(model_results)
            histogram = model_results.value_counts().reset_index()
            st.write(histogram)
            st.write(histogram.columns)
            histogram.columns = ['Output', 'Count']
            chart = alt.Chart(histogram).mark_bar().encode(x='Output', y='Count')
            st.altair_chart(chart, use_container_width=True)