from dotenv import load_dotenv
import requests
import json 
import os
import pandas as pd 
import numpy as np
load_dotenv()

df = pd.read_csv('data/fixed.csv', on_bad_lines="skip", encoding='utf-8')

def read_and_sample_df(alarm_group_id):
    df_sample= df[df['alarm_group_id']== alarm_group_id]
    # Drop columns with null values 
    cols = ['alarm_name', 'start_time', 'content', 'addition_info', 'vendor_name']
    df_sample = df_sample[cols]
    sample_dict = df_sample.to_dict(orient="records")
    sample_json = json.dumps(sample_dict, ensure_ascii=False, indent=2)
    return sample_json

alarm_group_ids = df['alarm_group_id'].unique()
alarm_instruction = ""
with open('data/backlog.txt', 'r', encoding='utf-8') as f:
    alarm_instruction = f.read()
        
for i, alarm_group_id in enumerate(alarm_group_ids):
    print(f"Processing {i+1}/{len(alarm_group_ids)}: {alarm_group_id}")
    sample_json = read_and_sample_df(alarm_group_id=alarm_group_id)
    url = "https://netmind.viettel.vn/dgx-qwq/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('QWEN_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen/Qwen3-30B-A3B-Instruct-2507-FP8-server-78",
        "messages": [
            {"role": "system", "content": f"""
    Bạn là một trợ lý AI chuyên phân loại cảnh báo mạng IP. 
    Dưới đây là kiến thức tham khảo về các loại cảnh báo phổ biến:
    {alarm_instruction}

    Nhiệm vụ: Khi nhận dữ liệu cảnh báo từ một nhóm alarm_group_id, 
    hãy đưa ra một tên nhóm cảnh báo tổng quát,và có tính đại diện 
    cho toàn bộ nhóm. 
    Chỉ đưa ra tên tổng quát bằng tiếng Anh, không cân giải thích thêm.
    """},

            {"role": "user", "content": f"""
    Dưới đây là dữ liệu cảnh báo thuộc cùng một alarm_group_id:
    {sample_json}
    """}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    df.loc[df['alarm_group_id']==alarm_group_id, 'group_name'] = response.json()["choices"][0]["message"]["content"]
    # print(response.status_code)
    # print(response.json()["choices"][0]["message"]["content"])
    # Save df 
    df.to_csv('data/fixed.csv', index=False, encoding='utf-8')