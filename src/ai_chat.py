from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型v3.5的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '2602f1de'
SPARKAI_API_SECRET = 'YjY2ZmZjZDM5NzhlNmM3ZDhmZTRlMzYy'
SPARKAI_API_KEY = '2ee9672540bd7a082718aa810fead544'
#星火认知大模型v3.5的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'
def chat(file_path):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False ,
    )
    with open(file_path+'\\data\\comments.txt', 'r',encoding='utf-8') as file:  # 打开文件
        comments_text = file.read()
        #print(comments_text)
    with open(file_path+'\\data\\pre.txt', 'r',encoding='utf-8') as file:  # 打开文件
        pre_text = file.read() 

    messages = [ChatMessage(
        role="user",
        content = pre_text + comments_text
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0]
