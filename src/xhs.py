# 导入所需的库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import time
import spark_chat
import gpt_chat
import re
from time import sleep
import os
import tkinter as tk
from tkinter import ttk, messagebox

#设置文件夹
file_path = r'D:\\programs\\web_auto_xiaohongshu'


# 等待元素加载的函数
def wait_for_elements(driver, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_all_elements_located(locator))
        return 1
    except TimeoutException:
        return 0

# 退出页面的函数
def exit_page():
    driver.close()
    handles = driver.window_handles  # 获取当前浏览器的所有窗口句柄
    driver.switch_to.window(handles[0])

def send_message(message):
        t = wait_for_elements(driver, (By.XPATH, "//div[@class='inner']"), 10)
        
        # 定位可编辑区域
        editable_div = driver.find_element(By.XPATH, "//div[@class='inner']")  
        
        # 点击可编辑区域
        editable_div.click()

        t = wait_for_elements(driver, (By.ID, "content-textarea"), 10)

        ele = driver.find_element(By.ID, "content-textarea")

        # 点击该元素以确保其成为焦点
        ele.click()  # 点击以激活编辑区域

        ele.send_keys(message)  # 输入文本

        # 等待提交按钮加载
        t = wait_for_elements(driver, (By.CSS_SELECTOR, "button.btn.submit"), 10)

        submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn.submit")
        submit_button.click()
        sleep(1)

# 获取评论内容并写入文件
def get_comment(n,driver):
    # 等待页面加载
    time.sleep(1)
    #打印标题
    ele = driver.find_element(By.XPATH, "//div[@class='note-content']")
    print(ele.text)
    try:
        total_comments_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".total"))
        )
        total_comments_text = total_comments_element.text
        print(f"总评论数（包括回复）: {total_comments_text}")
    except Exception as e:
        print("无法找到总评论数元素", e)
        driver.quit()
        return

    comments = []
    comments_texts = []
    
    action = ActionChains(driver)
    report_div = driver.find_element(By.XPATH, "//div[@class='notedetail-menu']")
        
    # 点击举报键(定位评论区)
    report_div.click()
    report_div.click()
    #防止实际评论过少导致一直循环，若评论数一直为某一数字，则停止爬取
    repeat_flag = 0
    repeat_num = 0
    
    while len(comments) < n:
        # 获取所有的评论元素
        comments = driver.find_elements(By.CLASS_NAME, 'parent-comment')

        print(f"当前评论数: {len(comments)}")

        if len(comments) == repeat_num:
            repeat_flag += 1
        else:
            repeat_flag = 0
        repeat_num = len(comments)
        #print("-----------")
        #向下滚动评论区
        video_flag = driver.find_elements(By.CLASS_NAME, 'xgplayer-icon-play')
        if video_flag:
            action.send_keys(Keys.PAGE_DOWN).perform() 
        else:
            action.send_keys(Keys.SPACE).perform()
        if repeat_flag > 20:
            break
    #返回页面顶部
    action.send_keys(Keys.HOME).perform()

    # 遍历并读取前n个评论以及回复内容
    for i in range(min(n, len(comments))):
        comment = comments[i]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment)
        # 获取评论作者
        #author = comment.find_element(By.CSS_SELECTOR, '.author .name').text
        # 获取评论内容
        content = comment.find_element(By.CSS_SELECTOR, '.content').text 
        comments_texts.append("评论"+str(i+1)+": "+content)
        
        '''# 获取评论时间和位置
        date = comment.find_element(By.CSS_SELECTOR, '.date').text
        location = comment.find_element(By.CSS_SELECTOR, '.location').text
        # 获取点赞数量
        likes = comment.find_element(By.CSS_SELECTOR, '.like .count').text
        # 获取回复数量
        replies = comment.find_element(By.CSS_SELECTOR, '.reply .count').text'''
        # 打印或处理评论内容
        print(f'评论 {i + 1}:')
        #print(f'作者: {author}')
        print(f'内容: {content}')
        #print(f'时间: {date}')
        #print(f'位置: {location}')
        #print(f'点赞数: {likes}')
        #print(f'回复数: {replies}')
        print('-----------------------')
        #获取楼中楼
        show_more_button_flag = 0
        while show_more_button_flag < 5:
            try:
                # 在指定的父元素（评论元素）内查找“显示更多”按钮
                show_more_button = WebDriverWait(comment, 1).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@class='show-more']"))
                )
                # 定位“显示更多”按钮并滚动到可见
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_button)

                # 点击“显示更多”按钮
                show_more_button.click()
                show_more_button_flag += 1

            except:
                print("无更多回复")
                # 如果找不到“显示更多”按钮，跳出循环
                break

        if show_more_button_flag > 0:
            # 获取回复元素
            replys = comment.find_element(By.CLASS_NAME, 'reply-container')
            reply = replys.find_elements(By.CLASS_NAME, 'content')
            for i in range(len(reply)):
                # 获取回复内容
                reply_content = reply[i].text
                print(f"回复{i+1}: {reply_content}")
                comments_texts.append("回复"+str(i+1)+": "+reply_content)

            #print(show_more_button_flag)
        show_more_button_flag = 0
    # 写入评论内容到文件
    with open(file_path+'\\data\\comments.txt', 'w', encoding='utf-8') as file:
        file.write(ele.text + '\n')
        for comment in comments_texts[:n]:  
            file.write(comment + '\n')

def chosse_model(file_path):
    # 创建主窗口
    root = tk.Tk()
    root.title("AI 模型选择器")



def ai_message():
     #打开评论区文档
        file_answer = file_path+'\\data\\answer.txt'   # 指定文件路径

        answer = spark_chat.chat(file_path)
        print(answer)
        answer = gpt_chat.chat(file_path)
        print(answer)
        with open(file_answer, 'w', encoding='utf-8') as file:
            file.write(answer + '\n')

# 设置浏览器类型
browser = 'chrome'

# 设置浏览器远程调试端口
port = {
    'chrome':'9529',
    'edge':'9222'
}

# 设置浏览器程序路径
directory_path = {
    'chrome':'C:/Program Files/Google/Chrome/Application',
    'edge':'C:/Program Files (x86)/Microsoft/Edge/Application'
}

# 设置命令
command = {
    'chrome':'chrome.exe --remote-debugging-port=' + port[browser] + ' --user-data-dir="D:\programs\web_auto\chrome_profile"',
    'edge':'msedge.exe --remote-debugging-port=' + port[browser] + ' --user-data-dir="D:\programs\web_auto\edge_profile"'
}

# 切换工作目录并启动浏览器进程
os.chdir(directory_path[browser])
process = subprocess.Popen(command[browser], shell=True)
sleep(2)
process.terminate()

# 根据浏览器类型选择对应的webdriver
if browser == 'chrome':
    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + port[browser] )
    driver = webdriver.Chrome(options=options)
elif browser == 'edge':
    options = EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + port[browser] )
    driver = webdriver.Edge(options=options)
else:
    raise ValueError("Invalid browser choice")

# 打开指定网页
url = 'https://www.xiaohongshu.com/explore'#小红书官网首页
driver.get(url)

# 最大化浏览器窗口
driver.maximize_window()

#循环次数，可以根据需要设置，建议不要太大，防止被封IP
n = 10
while (1):
    flag = 1
    comment_num = 50 #读取评论数目
    #获取标题 
    titles = driver.find_elements(By.CSS_SELECTOR, "a.title")
    if not titles:
        break

    # 遍历所有标题
    for title in titles:
        # 获取链接文本
        title_text = title.text
        #print(title_text)  # 打印标题
        try:
            title.click()  # 点击链接
            handles = driver.window_handles #获取当前浏览器的所有窗口句柄
            driver.switch_to.window(handles[-1])    #切换到最新打开的窗口
            get_comment(comment_num,driver)
            ai_message()
            #send_message("啊")
            
            driver.back()  # 关闭弹窗
            n -=1  # 循环次数减一
            if n == 0:
                break
        except Exception as e:
            print(e)
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
            driver.back()  # 关闭弹窗
            break
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()#向下滚动页面
    time.sleep(1)



