import os
import requests
import json
API_KEY = os.getenv("BAIDU_API_KEY")
SECRET_KEY = os.getenv("BAIDU_API_SECRET")


def analyse(str):
        
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + get_access_token()
    
    payload = json.dumps({
        "text": str
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    return response.text

'''
参数	        说明     描述
log_id          uint64  请求唯一标识码
sentiment	    int	    表示情感极性分类结果，0:负向，1:中性，2:正向
confidence	    float	表示分类的置信度，取值范围[0,1]
positive_prob	float	表示属于积极类别的概率 ，取值范围[0,1]
negative_prob	float	表示属于消极类别的概率，取值范围[0,1]


{
    "text":"我爱祖国",
    "items":[
        {
            "sentiment":2,    //表示情感极性分类结果
            "confidence":0.90, //表示分类的置信度
            "positive_prob":0.94, //表示属于积极类别的概率
            "negative_prob":0.06  //表示属于消极类别的概率
        }
    ]
}
'''

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))