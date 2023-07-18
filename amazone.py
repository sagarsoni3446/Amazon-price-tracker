import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os#for checking the path of the file
import time#for sleeping the programme for some time 
##link of the product
url = 'https://www.amazon.in/dp/B0C788SHHC?ie=UTF8&ref_=hero1_narzo60&pf_rd_r=RXNSYCRNA7973T4B03A2&pf_rd_p=d4a2ae4d-dee1-4782-affb-109827f1df39&pd_rd_r=ee6ad244-8bd5-486d-900d-146a0edecc62&pd_rd_w=gkHGa&pd_rd_wg=iv6Ka'

## this will include the data about the web browser
headers = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

def check_phone_price():
    ##request model to reach the page
    page = requests.get(url,headers=headers)

    ##now using beautiful soup to extract the page as HTML
    bs = BeautifulSoup(page.content, 'html.parser')

    #print(bs.prettify()).encode("utf-8")
    ## Extracting the product name from the web page
    ##used get text to remove the garbage texts
    product_title = bs.find(id="productTitle").get_text()

    ##used strip() to get rid of extra spaces
    #print(product_title.strip())

    #extracted the price from the web page
    price=bs.find('span',{'class':'a-price-whole'}).get_text()
    price = price.replace(",","")
    price = price.replace(".","")
    price_float = float(price)
    #print(price_float)

    file_exists = True
    if not os.path.exists("./price.csv"):
        file_exists = False

    with open("price.csv","a") as file:
        writer  = csv.writer(file,lineterminator='\n')
        fields = ["Timestamp","price(AED)"]
        if not file_exists:
            writer.writerow(fields)
        
        timestamp = f"{datetime.datetime.date(datetime.datetime.now())}, {datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp, price_float])
        print("wrote data to file")


    return price_float

def send_email():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    #for ecryting the trafic we use starttls()
    server.starttls()
    server.ehlo()
    #now loging into google account
    server.login('uploadfile141@gmail.com',"S84618631")

    subject = "Hey! the price fell down. Do you wanna buy"
    body = "Go order now before the price fluctuates\n Link:https://www.amazon.in/dp/B0C788SHHC?ie=UTF8&ref_=hero1_narzo60&pf_rd_r=RXNSYCRNA7973T4B03A2&pf_rd_p=d4a2ae4d-dee1-4782-affb-109827f1df39&pd_rd_r=ee6ad244-8bd5-486d-900d-146a0edecc62&pd_rd_w=gkHGa&pd_rd_wg=iv6Ka"
    msg = f"subject: {subject}\n\n\n\{body}"

    server.sendmail('uploadfile141@gmail.com','uploadfile141@gmail.com',msg)
    print("email sent")
    server.quit()
while True:
    price = check_phone_price()
    if(price<17500):
        send_email()
    time.sleep(36000)#take inputs in secs