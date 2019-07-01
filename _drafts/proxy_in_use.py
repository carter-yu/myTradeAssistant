import requests
import mechanicalsoup


proxies = {
#    'https': '163.172.217.103:3128',
    'https': '159.65.110.167:3128'
}

url = "https://www.iplocation.net/find-ip-address"
#url = "https://www.reuters.com/finance/markets/index/.IXIC"
url = "http://www.nasdaq.com/symbol/nvda"
Session = requests.Session()
browser = mechanicalsoup.StatefulBrowser()
browser.session.proxies = proxies
browser.open(url)
reutersUsStockPage = browser.get_current_page()
#print(reutersUsStockPage.findAll("span",  attrs={"style": "font-weight: bold; color:green;"}))
#[<span style="font-weight: bold; color:green;">219.78.213.42</span>]
print(reutersUsStockPage.findAll("h1"))