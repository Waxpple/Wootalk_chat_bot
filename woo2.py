# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 00:46:08 2021

@author: Ethan
"""

# -*- coding: utf-8 -*-
import sys  
import os
import time
from selenium import webdriver
import json
import requests
import random
import urllib
from opencc import OpenCC
import json

# Use your hugging face API to reply the answer.
API_URL = "https://api-inference.huggingface.co/models/wptoux/albert-chinese-large-qa"
headers = None ###


def qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]

def query(payload):
	data = json.dumps(payload)
	response = requests.request("POST", API_URL, headers=headers, data=data)
	return json.loads(response.content.decode("utf-8"))


def sendMessage(text):
    textBox = driver.find_element_by_id('messageInput')
    textBox.send_keys(str(text))
    driver.find_element_by_id('sendButton').click()
    return
def leave():
	driver.find_element_by_id('changeButton').click()
	time.sleep(0.5)
	##if the user left, the popup message won't be displayed###
	try:
		driver.find_element_by_id('popup-yes').click()
	except:
		pass

def dochat():##chatbot starts to do its job =)##
    try:
        driver.find_element_by_class_name('buttons').click()
    except:
        pass
    time.sleep(1)
    strangerText = None
    tempText = None
    timeoff = 0
    while(True):
        try:
            try:
                checkLeave = driver.find_elements_by_class_name("system")
                for i in checkLeave:
                    if i.text.find("對方離開")!=-1:
                        leave()
                        return
            except:
                pass
            
            strangerText = driver.find_elements_by_css_selector(".stranger.text")
            strangerText = strangerText[-1]
            strangerText = str(strangerText.text).replace('\n','').replace('(','').replace(' ','').replace('剛剛)','').replace('分前','').replace('陌生人：','').replace('行動裝置','').replace('App','')  
            if tempText != strangerText:
                #Do response
                """data = query(
                            {
                                "inputs": {
                                    "question": strangerText.text,
                                    "context": "我19歲。我是女大學生。住在台北。平常都在滑wootalk。喜歡打羽球>//<。",
                                }
                            }
                        )
                sendMessage(data['answer'].replace(' ',''))
                """
                time.sleep(float(random.randint(0,15)))
                if 'hi' in strangerText or 'Hi' in strangerText or '嗨' in strangerText or '你好' in strangerText or '安安' in strangerText or '哈囉' in strangerText or '男' in strangerText:
                    sendMessage("嗨！19女")
                elif '?' == strangerText or '？' == strangerText:
                    sendMessage("說些有趣的，憑實力單身嘛")
                else:
                    try:
                        sendMessage(bag_of_word[strangerText])
                    except:
                        msg = req_trans.convert(strangerText)
                        res = qingyunke(msg)
                        sendMessage(ans_trans.convert(res))
                        bag_of_word.update( {strangerText: ans_trans.convert(res) })
                        # try:
                        #     ans = bag_of_word[strangerText]
                        #     sendMessage(ans)
                        # except:
                        #     ans = ["我不知道欸 ‹‹\(´ω` )/›› 問點別的吧", "你勒♡(*´∀｀*)人(*´∀｀*)♡","不告訴你( • ̀ω•́ )","(´∩ω∩｀)你猜呀","δ△δ那是甚麼?"]
                        #     sendMessage(ans[random.randint(0,len(ans)-1 )])
                        #     bag_of_word.update( {tempText: strangerText })
                timeoff = 0
                tempText = strangerText
                
                print("temp:",tempText,"Now",strangerText)
                print(bag_of_word)
            else:
                
                raise 'error'
            

        except:
            print(timeoff)
            timeoff += 1
            if timeoff > 200:
                leave()
                break
            time.sleep(0.1)
            pass
            
        

    


chromedriver = r".\chromedriver.exe"  # YOUR chromedriver PATH
os.environ["webdriver.chrome.driver"] = chromedriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
driver.get("https://wootalk.today/")
time.sleep(1) ##time for human verification. =D
driver.find_element_by_class_name('buttons').click()
time.sleep(1) ##time for human verification. =D
driver.refresh()
BETA = True

req_trans = OpenCC('t2s')
ans_trans = OpenCC('s2t')
bag_of_word = {'哈囉':'嗨'}
try:
    with open('data2.json', 'r') as fp:
        bag_of_word = json.load(fp)
except:
    print("first time use it huh?")
    pass
fp.close()

while(True):
    if BETA:
        driver.get("https://wootalk.today/key/CHATBOT")
    else:
        driver.get("https://wootalk.today/")
        pass
        
    dochat()
    time.sleep(1) ##time for human verification. =D
    driver.refresh()
    with open('data2.json', 'w') as fp:
        json.dump(bag_of_word, fp)

fp.close()
