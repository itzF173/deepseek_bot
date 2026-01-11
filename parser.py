from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telebot import types, TeleBot
from urllib.parse import quote_plus
import requests
import random
import time
import numpy as np

new = "8244416237:AAHezGXRITlbKHsNQXFJIFWG2dNheB8gR70"
bot = TeleBot(new)































# @bot.message_handler(commands=['img'])
# def sendImg(m):
#     prompt = m.text.partition(' ')[2].strip() #чисты запрос после пробела
#     bot.send_message(m.chat.id, "Ищу...")
#     #генерим рандомное число
#     seed = random.randint(0, 2_000_000_000)
#     print(seed)
#     # улучшение запроса
#     q = quote_plus(f"{prompt}, high quality, very detailed, soft light")

#     url = f"https://image.pollinations.ai/prompt/{q}?width=500&height=500&seed={seed}&n=1"
#     res = requests.get(url, timeout=90, allow_redirects=True)
#     bot.send_photo(m.chat.id, res.content)



# @bot.message_handler(commands=['start'])
# def cmd_start(message):
#     bot.send_message(message.chat.id,"Hello, i'm parsing bot. Try it by /search command for search")

#@bot.message_handler(commands=['search'])
#def cmd_search(message):
#    bot.send_message(message.chat.id,"Send URl in chat")





#@bot.message_handler(content_types=['text'])
def get_text(message):
    txt = message.text
    print(txt)
    #bot.send_message(message.chat.id, txt)
    #print(txt.find("search",0,str.__len__(txt)))
    if(txt.find("/parse",0,str.__len__(txt))!=-1):
        print(txt)
        #bot.send_message(message.chat.id,txt,parse_mode='Markdown')
        name = txt.replace("/parse ","")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.wildberries.ru/catalog/0/search.aspx?search="+name)
        quote_box = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.CLASS_NAME, "product-card-list"))
         )
        cards__names = quote_box.find_elements(By.CLASS_NAME, "product-card__name")
        prices = quote_box.find_elements(By.CLASS_NAME, "price__wrap")
        URLsClasses = quote_box.find_elements(By.CLASS_NAME, "product-card__link.j-card-link.j-open-full-product-card")
        i = 0
        URLs = []
        while i < len(URLsClasses):
            URLs.append(URLsClasses[i].get_attribute("href"))
            #print(URLs[i])
            i+=1
        #print(URLs[1])
        i = 0
        allitems = cards__names
        #while i < len(cards__names):
       #     allitems.__add__(cards__names[i].text)
        #i = 0
        items = []

        i = 0
        pricesNoRub = np.array([])
        while i < len(prices):
            block = prices[i].text.split("₽",len(prices[i].text))
            #print(block)
            fin = block[0].replace(" ", "")
            pricesNoRub = np.append(pricesNoRub,fin)
            #print(pricesNoRub[i])
            i+=1
        i = 0
        prices2 = []
        while(i < len(pricesNoRub)):
            prices2.append(pricesNoRub[i])
            i+=1
        #prices2 = pricesNoRub
        i = 0
        min = []
        minCur = 0
        # while i < len(pricesNoRub):
        #     if(len(max) == 0):
        #         #print("0")
        #         max.append(pricesNoRub[i])
        #
        #
        #     if(pricesNoRub[i]>max[len(max)-1]):
        #         #print(pricesNoRub[i])
        #         max.append(pricesNoRub[i])
        #
        #
        #     #pricesFor.append(float(pricesNoRub).max())
        #     #np.delete(pricesNoRub,float(pricesNoRub).max())
        #     #print(pricesFor[i])
        #     i+=1
        # pricesFor = max
        #print("0")
        while i < len(pricesNoRub):
            j = 0
            k = 0
            #print("1")
            while j < len(prices2):
                #print(j)
                if(float(prices2[j])<minCur or minCur == 0):
                    minCur = float(prices2[j])
                    k = j
                j+=1

            min.append(minCur)
            minCur = 0
            prices2.remove(prices2[k])
            #print(i)
            #print(min)
            #print(prices2)
            i+=1

        #print(pricesFor)
        #print(max)
        i = 0
        #print("0")
        while i < len(min):
            j= 0
            #print("0.5")
            while j < len(min):

                cur = str(min[i])
                #cur = str.replace(cur,".0","")
                #print(allitems[j].text.find(cur, 0, len(cur)))
                #print(allitems[j].text)
                #print(cur)
                #print(len(cur))
                #print(cur.find(".0",0,len(cur)))
                cur2 = cur.split(".",1)[0]
                #print(cur2)
                #print(cur.replace(".0", ""))
                #print(prices[j].text + " " + cur2)

                price = prices[j].text.replace(" ", "")
                if(price.find(cur2)!=-1):
                    items.append(allitems[j].text + " " + cur2 + "₽ " + URLs[j])
                    #print("1")
                j+=1
            i+=1
        # i = 0
        # while i < len(allitems):
        #     if(allitems[i].text.find(name,0,len(allitems[i].text))!=-1):
        #         items.append(allitems[i].text + " " + prices[i].text + " " + URLs[i])
        #         #print(items[i])
        #     i+=1
        i = 0
        
        while i < len(items):
            bot.polling()
            bot.send_message(message.chat.id,items[i])
            
            #print(items[i])

            i+=1
        bot.stop_polling()
#product-card__name
#bot.infinity_polling()

# driver.get("https://quotes.toscrape.com/")
#
# quote_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "quote"))
# )
# quotes = driver.find_elements(By.CLASS_NAME, "quote")
# for quote in quotes:
#     txt = quote.find_element(By.CLASS_NAME, "text").text
#     print("Цитата: "+txt)
#print(quotes)

class simpleParser:
    def Parce(msg):
        get_text(message=msg)