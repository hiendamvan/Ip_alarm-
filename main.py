import requests
import os
from dotenv import load_dotenv
import pandas as pd 
import numpy as np
load_dotenv()

def read_and_sample_df(idx):
    df = pd.read_csv('data/fixed.csv', on_bad_lines="skip", encoding='utf-8')
    sample = df.iloc[idx]
    # Drop columns with null values 
    sample = sample.dropna()
    flattened_sample = ', '.join([f"{col}: {sample[col]}" for col in sample.index])
    return flattened_sample

sample = read_and_sample_df(0)
alarm_instruction = ""
with open('data/backlog.txt', 'r', encoding='utf-8') as f:
    alarm_instruction = f.read()
    
url = "https://netmind.viettel.vn/dgx-qwq/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('QWEN_API_KEY')}",
    "Content-Type": "application/json"
}
payload = {
    "model": "Qwen/Qwen3-30B-A3B-Instruct-2507-FP8-server-78",
    "messages": [
        {"role": "system", "content": f'''
         Bạn là một trợ lý AI giúp nhận diện và xử lí cảnh báo mảng IP. 
         Dưới đây là thông tin về một số loại cảnh báo phổ biến:{alarm_instruction}
        '''},
        {"role": "user", "content": "Dưới đây là một cảnh báo cụ thể. Hãy đưa ra nguyên nhân gốc của cảnh báo này, không cần reasoning!" + sample}
    ],
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload, timeout=60)

print(response.status_code)
print(response.json()["choices"][0]["message"]["content"])
