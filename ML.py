import pandas as pd
import joblib
from text_preprocessing import text_normalizer
import multiprocessing
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import os
from datetime import datetime, timedelta
import pytz


num_cores = multiprocessing.cpu_count()-1

def parallel_normalizer_apply(chunk):
    return chunk.apply(text_normalizer)


def categorize_new_data(raw_data_file, categorized_data_file):
    raw_df = pd.read_csv(raw_data_file)
    try :
        categorized_df = pd.read_csv(categorized_data_file)
    except:
        categorized_df = pd.DataFrame({
            'link':[],
            'description':[],
            'date':[]
        })
    
    new_rows = raw_df[~raw_df['date'].isin(categorized_df['date'])].reset_index(drop=True)
    if new_rows.empty == True:
        del categorized_df
        del raw_df
        del new_rows
        return

    text_normalizer, classify_text, svm_model, label_mapping_dict = joblib.load(os.path.join(os.getcwd(),'pipeline.pkl'))

    chunks = np.array_split(new_rows['description'], num_cores)

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(parallel_normalizer_apply, chunks))
    temp_df = pd.DataFrame()
    temp_df['description'] = pd.concat(results)
    vectorized_text = classify_text.transform(temp_df['description'].astype(str).tolist())
    predicted_categories = svm_model.predict(vectorized_text)
    temp_df['label'] = pd.DataFrame(predicted_categories)
    inverted_dict = {v: k for k, v in label_mapping_dict.items()}
    temp_df['label'] = temp_df['label'].map(inverted_dict)
    new_rows = pd.concat([
        new_rows,
        temp_df[['label']]
    ],  axis=1, join='outer')
    categorized_df = pd.concat([new_rows,categorized_df])

    categorized_df.date = pd.to_datetime(categorized_df['date'])
    
    cut_off_time = datetime.now(pytz.UTC) - timedelta(hours=48)
    
    categorized_df[categorized_df['date']>cut_off_time]
    
    categorized_df.to_csv(categorized_data_file, index=False)

categorize_new_data(
    os.path.join(os.getcwd(),'raw_data.csv'), 
    os.path.join(os.getcwd(),'categorized_data.csv')
    )


