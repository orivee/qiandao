import re
import requests
from bs4 import BeautifulSoup
import time


class SouShu8Login:
    userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

    def __init__(self, hostname, username, password, questionid='0', answer=None, proxies=None):
        self.session = requests.session()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.questionid = questionid
        self.answer = answer
        self.proxies = proxies

    @classmethod
    def user_qiandao(cls, hostname, username, password, questionid='0', answer=None, proxies=None):
        user = SouShu8Login(hostname, username, password, questionid, answer, proxies)
        user.login()
        user.space()
        user.credit()

    def form_hash(self):
        rst = self.session.get(f'https://{self.hostname}/member.php?mod=logging&action=login').text
        loginhash = re.search(r'<div id="main_messaqge_(.+?)">', rst).group(1)
        formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rst).group(1)
        return loginhash, formhash

    def login(self):
        headers = {
            "origin": f'https://{self.hostname}',
            "referer": f'https://{self.hostname}/',
            "user-agent": self.userAgent,
        }
        loginhash, formhash = self.form_hash()
        login_url = f'https://{self.hostname}/member.php?mod=logging&action=login&loginsubmit=yes&loginhash={loginhash}&inajax=1'
        form_data = {
            'formhash': formhash,
            'referer': f'https://{self.hostname}/',
            'loginfield': self.username,
            'username': self.username,
            'password': self.password,
            'questionid': self.questionid,
            'answer': self.answer,
            'cookietime': 2592000
        }
        login_rst = self.session.post(login_url, proxies=self.proxies, data=form_data, headers=headers)
        if self.session.cookies.get('yj0M_ada2_auth'):
            print(f'Welcome {self.username}!')
        else:
            raise ValueError('Verify Failed! Check your username and password!')

    def credit(self):
        headers = {
            "user-agent": self.userAgent,
        }
        credit_url = f"https://{self.hostname}/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu"
        credit_rst = self.session.get(credit_url).text
        credit_soup = BeautifulSoup(credit_rst, "lxml")
        hcredit_2 = credit_soup.find("span", id="hcredit_2").string

        print("昵称: %s 银币: %s" % (self.username, hcredit_2))

    def space_form_hash(self):
        rst = self.session.get(f'https://{self.hostname}/home.php').text
        formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rst).group(1)
        return formhash

    def space(self):
        headers = {
            "origin": f'https://{self.hostname}',
            "referer": f'https://{self.hostname}/home.php',
            "user-agent": self.userAgent,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        formhash = self.space_form_hash()
        space_url = f"https://{self.hostname}/home.php?mod=spacecp&ac=doing&handlekey=doing&inajax=1"

        for x in range(5):
            form_data = {
                "message": "开心赚银币 {0} 次".format(x + 1).encode("GBK"),
                "addsubmit": "true",
                "spacenote": "true",
                "referer": "home.php",
                "formhash": formhash
            }
            resp = self.session.post(space_url, proxies=self.proxies, data=form_data, headers=headers)
            if re.search("操作成功", resp.text):
                print('第 {} 次发布成功!'.format(x + 1))
            time.sleep(120)


if __name__ == '__main__':
    SouShu8Login.user_qiandao('waterfire.allbookdown.com', 'username', 'password')
