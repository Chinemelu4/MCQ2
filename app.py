import streamlit as st
import pandas as pd
import numpy as np
import random
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load your dataset
df = pd.read_parquet('all_models.parquet')

st.title('Data Sampling App')   

specialties = df['specialty'].unique()
selected_specialty = st.selectbox('Select Specialty:', specialties)
model = st.selectbox('Select Model:', df['model'].unique())
question = st.selectbox('Select Question:', df['question_type'].unique())

if st.button('Generate Sample'):
    filtered_df = df[(df['specialty'] == selected_specialty) & (df['model'] == model) & (df['question_type'] == question)]
    filtered_true = filtered_df[filtered_df['correct'] == 1]
    filtered_false = filtered_df[filtered_df['correct'] == 0]
    num = np.random.randint(10000)

    # if len(filtered_true) > 2:
    #     filtered_true = filtered_true.sample(n=5,random_state=num)
    if len(filtered_false) > 20:
        filtered_false = filtered_false.sample(n=20,random_state=num)
    else:
        filtered_false = filtered_false 

        
    
    true_false_df = pd.concat([filtered_true, filtered_false],ignore_index=True)
    filtered_false.reset_index(drop=True,inplace=True)
    filtered_false.drop(['sample_id','user_id'], axis=1, inplace=True)
    #st.write(true_false_df[['sample_id', 'question', 'correct_answer2', 'model', 'model_answer', 'Correct and consistent with scientific consensus',
    # st.write(filtered_false[['sample_id', 'question', 'correct_answer2', 'model', 'model_answer', 'Rationale', 'Correct and consistent with scientific consensus',
    #    'Requires African local expertise', 'Omission of relevant info',
    #    'Includes irrelevant- wrong- or extraneous information',
    #    'Evidence of correct reasoning or logic',
    #    'Indication of demographic bias', 'Possibility of harm',
    #    'Question Quality', 'Formatting- style- structure or grammar issues']])
    
    st.write(filtered_false)
    def convert_df_to_csv(df1):
        return df1.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(filtered_false)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='sample_data.csv',
        mime='text/csv'
    )
