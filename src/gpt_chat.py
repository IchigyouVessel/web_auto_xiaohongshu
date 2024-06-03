import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat(file_path):
    with open(file_path+'\\data\\comments.txt', 'r',encoding='utf-8') as file:  # 打开文件
        comments_text = file.read()
    with open(file_path+'\\data\\pre_gpt.txt', 'r',encoding='utf-8') as file:  # 打开文件
        pre_text_gpt = file.read()

    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",  # 使用你想要的模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": pre_text_gpt + comments_text}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer