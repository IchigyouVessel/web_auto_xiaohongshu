#每隔30天重置一次access_token
import requests
import json


def main():
    file_path = 'd:\\programs\\web_auto_xiaohongshu'
    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=sxnKSynoO1xYFDwpvg8RItGu&client_secret=YjayIsmFtbCL1SQH6RbRJk3Z02ZAK5zd&grant_type=client_credentials"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    with open(file_path+'\\data\\baidu_access.txt', 'w', encoding='utf-8') as file:
        file.write(response.text + '\n')
    

if __name__ == '__main__':
    main()
