import re
import requests


class DiscuzLogin:
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    }

    def __init__(self, hostname, username, password, questionid='0', answer=None, proxies=None):
        self.session = requests.session()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.questionid = questionid
        self.answer = answer
        if proxies:
            self.proxies = proxies

    @classmethod
    def user_login(cls, hostname, username, password, questionid='0', answer=None, proxies=None):
        user = DiscuzLogin(hostname, username, password, questionid, answer, proxies)
        user.login()

    def form_hash(self):
        rst = self.session.get(f'https://{self.hostname}/member.php?mod=logging&action=login').text
        loginhash = re.search(r'<div id="main_messaqge_(.+?)">', rst).group(1)
        formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rst).group(1)
        return loginhash, formhash

    def login(self):
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
        login_rst = self.session.post(login_url, proxies=self.proxies, data=form_data)
        if self.session.cookies.get('xxzo_2132_auth'):
            print(f'Welcome {self.username}!')
        else:
            raise ValueError('Verify Failed! Check your username and password!')


if __name__ == '__main__':
    DiscuzLogin.user_login('hostname', 'username', 'password')