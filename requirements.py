# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)
slack_token = "xoxb-505014660117-507724408165-CsSqBOXUguHQYtBmkALBn52Z"
slack_client_id = "505014660117.507354560516"
slack_client_secret = "9c19dbac6b98a19fab2ee3677e762021"
slack_verification = "BXFSxBxr3cv1q8HVdqzsT8F7"
sc = SlackClient(slack_token)
# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    if ".com" in text:
        url =  re.search(r'(https?://\S+)', text.split('|')[0]).group(0)
    else:
        url = text
    if "naver" in url:
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        keywords=[]
        soup= soup.find_all("span",class_="ah_k")[:10]
        for i in range(len(soup)):
            keywords.append("%d위 : %s"%(i+1,soup[i].get_text().strip()))
        return u'\n'.join(keywords)
    
    elif "daum" in url:
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        keywords=[]
        soup= soup.find_all("a",class_="link_issue")[::2][:10]
        for i in range(len(soup)):
            keywords.append("%d위 : %s"%(i+1,soup[i].get_text().strip()))
        return u'\n'.join(keywords)
    elif "챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        top = soup.find("tbody",class_="tabItem champion-trend-tier-TOP")
        jungle = soup.find("tbody",class_="tabItem champion-trend-tier-JUNGLE")
        mid = soup.find("tbody",class_="tabItem champion-trend-tier-MID")
        adc = soup.find("tbody",class_="tabItem champion-trend-tier-ADC")
        support = soup.find("tbody",class_="tabItem champion-trend-tier-SUPPORT")
        topchamp=[]
        junglechamp =[]
        midchamp = []
        adcchamp=[]
        supportchamp = []
        topchamp.append("-------------------------")
        junglechamp.append("-------------champ rank")
        midchamp.append("----------")
        adcchamp.append("----------")
        supportchamp.append("------------------")
        
        topchamp.append("-------TOP----")
        junglechamp.append("------JUNGLE-----")
        midchamp.append("------MID-----")
        adcchamp.append("-----BOTTOM-----")
        supportchamp.append("-----SUP-----")
        
        for i in top.find_all("div",class_="champion-index-table__name"):
            topchamp.append(i.get_text())
        for i in jungle.find_all("div",class_="champion-index-table__name"):
            junglechamp.append(i.get_text())
        for i in mid.find_all("div",class_="champion-index-table__name"):
            midchamp.append(i.get_text())
        for i in adc.find_all("div",class_="champion-index-table__name"):
            adcchamp.append(i.get_text())
        for i in support.find_all("div",class_="champion-index-table__name"):
            supportchamp.append(i.get_text())
            
        topchamp.append("-------------------------")
        junglechamp.append("-------------CHAMP RANK")
        midchamp.append("----------")
        adcchamp.append("----------")
        supportchamp.append("------------------")

        keyword =[]
        for i in range(10):
            if i<2 :
                keyword.append(str(topchamp[i])+str(junglechamp[i])+str(midchamp[i])+str(adcchamp[i])+str(supportchamp[i]))
            else:
                x=str(topchamp[i].rjust(16))+str(junglechamp[i].rjust(16))+str(midchamp[i].rjust(16))+str(adcchamp[i].rjust(16))+str(supportchamp[i].rjust(16))
                keyword.append(x.center(86))
        return keyword

    elif "탑챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        top = soup.find("tbody",class_="tabItem champion-trend-tier-TOP")

        topchamp=[]

        topchamp.append("-----------TOP-----------")
        for i in top.find_all("div",class_="champion-index-table__name"):
            topchamp.append(i.get_text())
            
        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(topchamp[i]))
            else:
                x=str(topchamp[i].rjust(16)))
                keyword.append(x.center(86))
        return keyword
    elif "정글챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        jungle = soup.find("tbody",class_="tabItem champion-trend-tier-JUNGLE")

        junglechamp =[]

        junglechamp.append("-----------TOP-----------")
        for i in jungle.find_all("div",class_="champion-index-table__name"):
            junglechamp.append(i.get_text())
            
        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(junglechamp[i]))
            else:
                x=str(junglechamp[i].rjust(16)))
                keyword.append(x.center(86))
        return keyword
    
    elif "미드챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        mid = soup.find("tbody",class_="tabItem champion-trend-tier-MID")

        midchamp=[]

        midchamp.append("-----------TOP-----------")
        for i in mid.find_all("div",class_="champion-index-table__name"):
            midchamp.append(i.get_text())
            
        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(midchamp[i]))
            else:
                x=str(midchamp[i].rjust(16)))
                keyword.append(x.center(86))
        return keyword
    
    elif "바텀챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        adc = soup.find("tbody",class_="tabItem champion-trend-tier-ADC")

        adcchamp=[]

        adcchamp.append("-----------TOP-----------")
        for i in mid.find_all("div",class_="champion-index-table__name"):
            adcchamp.append(i.get_text())
            
        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(adcchamp[i]))
            else:
                x=str(adcchamp[i].rjust(16)))
                keyword.append(x.center(86))
        return keyword
    
    elif "서폿챔피언순위" in url:
        url = "https://www.op.gg/champion/statistics"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        support = soup.find("tbody",class_="tabItem champion-trend-tier-ADC")

        supportchamp=[]

        supportchamp.append("-----------TOP-----------")
        for i in support.find_all("div",class_="champion-index-table__name"):
            supportchamp.append(i.get_text())
            
        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(supportchamp[i]))
            else:
                x=str(supportchamp[i].rjust(16)))
                keyword.append(x.center(86))
        return keyword

    elif "랭킹순위" in url:
        driver = webdriver.Chrome(r"C:\Users\student\Downloads\chromedriver_win32\\chromedriver.exe")
        driver.get("http://www.op.gg/statistics/champion/")
        driver.find_element_by_css_selector('#statisticsChampionForm > table > tbody > tr > td:nth-child(2) > div > div:nth-child(1)').click()
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        topchamp=[]
        topchamp1=[]
        for i in soup.find_all("td",class_="Cell ChampionName"):
            topchamp.append(i.get_text().strip())
        for i in soup.find_all("span",class_="Value"):
            topchamp1.append(i.get_text().strip())
          

        keyword = []
        for i in range(10):
            if i<2 :
                keyword.append(str(topchamp[i])+"  "+str(topchamp1[i]))
            else:
                keyword.append(str(topchamp[i])+"  "+str(topchamp1[i]))
        return keyword
        
    
    
# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        
        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )
        return make_response("App mention message has been sent", 200,)
    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})
@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })
    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"
if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
