#-*- coding:utf-8 -*-
'''
FOR SBI STOCK BY WANGXG
'''
from abc import ABCMeta
import configparser
import requests
import re
import lxml.html
from bs4 import BeautifulSoup
from time import sleep

WAITING_TIME = 0.3

class Securities (metaclass=ABCMeta):
    """A securities provider."""

    def login(self):
        """Login the website."""
        pass

    # def get_top_page(self):
    #     """Get top page on website."""
    #     pass

    # def logout(self):
    #     """Logout the website."""
    #     pass

    # def portfolio_assets(self):
    #     """My portfolio."""
    #     pass

    # def stocks_sell_order(self, code, quantity, price):
    #     """Sell order."""
    #     pass

class SBIUser(Securities):
    
    def __init__(self):
        '''LOAD CONFIG INFO AND INIT '''
        config = configparser.ConfigParser()
        config.read('sbiconfig.ini')
        self.userid=config['login']['uid']
        self.password =config['login']['pwd']
        self.tpassword =config['login']['pwd2']

        self.headers = {
            'Accept': 'text/html',
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/56.0.2924.87 Safari/537.36'
        }
        self.session = requests.session()
        self.siteRoot = None

    def formLogin(self):
        """Login the website."""
        url_login='https://www.sbisec.co.jp/ETGate'
        custom = {
            'JS_FLG': '1',
            'BW_FLG': 'chrome,56',
            'ACT_login.x': '39',
            'ACT_login.y': '26',
            'user_id': self.userid,
            'user_password': self.password
        }
        r = self.session.get('https://www.sbisec.co.jp/ETGate', headers=self.headers)
        r.encoding = r.apparent_encoding
        
        soup = BeautifulSoup(r.text)
        form_login = soup.find(attrs={"name":"form_login"})   
        form_inputs = form_login.findAll('input')

        data = {i['name']:i['value'] for i in form_inputs if i.has_attr("value")}
        data.update(custom) #customでdicInputを更新
        
        sleep(WAITING_TIME)

        #POST送信            
        r = self.session.post(url_login, data=data, headers=self.headers)
        r.encoding = r.apparent_encoding
        return len(data) > len(custom), r 

    def formSwitch(self, htmltext):
        # 受け取ったページのformSwitchフォームを取り出す
        root = lxml.html.fromstring(htmltext)
        forms = root.xpath('//form[@name="formSwitch"]')
        
        form_attribute = forms[0].attrib
        act = form_attribute.get('action')

        form_inputs = root.xpath('//form[@name="formSwitch"]//input')
        data = {x.get('name'): x.get('value') for x in form_inputs}
        
        sleep(WAITING_TIME)
        # formSwitchフォームの内容をそのまま送信する
        r = self.session.post(act, data=data, headers= self.headers)
        r.encoding = r.apparent_encoding
        self.siteRoot = r.text;
        return len(data) > 2, r

    def redirect(self, a):
        """redirect to <a href=...>."""
        # リンクを取り出す
        link = 'https://site2.sbisec.co.jp' + a.get('href')
        sleep(WAITING_TIME)
        r = self.session.get(link, headers=self.headers)
        r.encoding = r.apparent_encoding
        return r.status_code == 200, r

    def logout(self, r):
        """Logout the website."""
        # a要素の子要素でalt属性が"ログアウト"のページを得る
        soup = BeautifulSoup(r.text)
        img = soup.find(title=re.compile("ログアウト"))
        a = img.parent
        return self.redirect(a)

    def getAByText(self, r, text):
        """get <a from r.text by text."""
        # a要素の子要素でalt属性が"ログアウト"のページを得る
        soup = BeautifulSoup(r.text)
        listA = soup.findAll('a', text=text)
        if len(listA) >0:
            return True, listA[0]
        else: 
            return False, None

    def getPortfolio(self, r):
        soup = BeautifulSoup(r.text)
        tdDeals= soup.findAll('td', text="取引")
        realTable = tdDeals[0].parent.parent
        credTable = tdDeals[1].parent.parent
        
        #株式（現物一般）
        rTRs = realTable.findAll('tr')

        #投資
        cTRs = credTable.findAll('tr')



if __name__ == "__main__":
    sbi = SBIUser()
    flag, r = sbi.formLogin()
    if flag: #login OK
        flag, r = sbi.formSwitch(r.text)
        flag, a = sbi.getAByText(r, "ポートフォリオ") 
        if flag:
            flag, r = sbi.redirect(a)

        #flag, r = sbi.logout(r)

    # if r.status_code == 200:
    #     soup = BeautifulSoup(r.text)
    #     print(soup)  

