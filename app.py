import pandas as pd
from sklearn.preprocessing import LabelEncoder
from shinywidgets import render_plotly
import plotly.express as px

from shiny.express import ui, input

ui.page_opts(fillable=True)

def preprocess(df: pd.DataFrame):
    cols_with_missing_vals = df.columns[df.isna().any()]
    for c in cols_with_missing_vals:
        df.drop(df.index[df[c].isna()], inplace=True)
    encoder = LabelEncoder()
    df['Motivation_Level'] = encoder.fit_transform(df['Motivation_Level'])

df = pd.read_csv('StudentPerformanceFactors.csv')
preprocess(df)


with ui.nav_panel("Explore variable distributions"):
    ui.input_selectize('var', 'Select your variable', choices=df.columns.to_list())
    
    with ui.card():
        @render_plotly
        def hist():
            return px.histogram(df, x=input.var(), template='simple_white')

with ui.nav_panel('Sleep v/s Exam Score'):
    
    with ui.card():
        score_dict = df.groupby(by=['Exam_Score'])['Exam_Score'].count().to_dict()
        df['score_freq']=df['Exam_Score'].map(score_dict)
        @render_plotly
        def plot():
            return px.scatter(data_frame=df, x='Sleep_Hours', y='Exam_Score', size='score_freq', color='score_freq' ,template='simple_white' )

with ui.nav_panel('Effects of extra-curricular activities'):
    mean_by_ea = df.groupby(by=['Extracurricular_Activities'], as_index=False)['Exam_Score'].mean()
    
    with ui.card():
        @render_plotly
        def _():
            return px.bar(data_frame=mean_by_ea, x='Extracurricular_Activities', y='Exam_Score', template='simple_white')
        
