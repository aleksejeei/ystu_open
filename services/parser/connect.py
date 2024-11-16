import requests
from bs4 import BeautifulSoup

def get_profile(login, password):
    html = requests.post('https://www.ystu.ru/WPROG/auth1.php', data={'login': login.strip(), 'password': password.strip()})
    html.encoding = 'windows-1251'
    return html.text

class connect: # класс с авторизацией и получением html страниц аккаунта
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.h = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Host': 'www.ystu.ru',
            'Origin': 'https://www.ystu.ru',
            'Referer': 'www.ystu.ru'
        }

        # создание сессии
        url_login = 'https://www.ystu.ru/WPROG/auth.php'
        h = self.h
        s = requests.Session()
        html = s.get(url_login, headers=h)
        soup = BeautifulSoup(html.text, 'html.parser')
        codeYSTU = soup.find('input', dict(name='codeYSTU'))['value']
        jsonp = {
            'codeYSTU': codeYSTU,
            'login': self.login,
            'password': self.password,
            'login1': '%C2%F5%EE%E4+%BB'
        }
        h['Referer'] = 'https://www.ystu.ru/WPROG/auth.php'
        s.post('https://www.ystu.ru/WPROG/auth1.php', data=jsonp, headers=h)
        self.s = s
        # создание сессии

    def auth(self): # создание авторизованной сессии
        s = self.s
        return s

    # def get_profile(self): # получение html страницы со всеми данными профиля
    #     session = self.auth()
    #     h = self.h
    #     h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
    #     info = session.get('https://www.ystu.ru/WPROG/lk/lkstud.php', headers=h)
    #     return info.content.decode('windows-1251')

    def get_marks(self): # получение html страницы с оценками
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
        info = session.get('https://www.ystu.ru/WPROG/lk/lkstud_oc.php', headers=h)
        return info.content.decode('windows-1251')

    def get_statements(self): # получение html страницы с заявками
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
        info = session.get('https://www.ystu.ru/WPROG/lk/lkorder.php', headers=h)
        return info.content.decode('windows-1251')

    def delete_placereq(self, number):
        html = self.get_statements()
        html_text = BeautifulSoup(html, 'html.parser')
        result = html_text.find_all('table')[0].find_all('tr')[int(number)]
        return result

    def get_schedule_sem(self):
        html = self.s.get('https://www.ystu.ru/WPROG/lk/lkstud.php')
        html_text = html.content.decode('windows-1251')
        html_soup = BeautifulSoup(html_text, 'html.parser')
        link = html_soup.find('a', attrs={'title': 'В расписание группы!'})['href']
        link_schedule = f'https://www.ystu.ru{link}'
        schedule_html = self.s.get(link_schedule).content.decode('windows-1251')
        return schedule_html

    def disconnect(self):
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/lk/lkstud.php'
        session.get('https://www.ystu.ru/WPROG/exit_ses.php', headers=h)


class statements:
    def __init__(self, login, password):
        self.s = connect(login, password).auth()
        self.h = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Host': 'www.ystu.ru',
            'Origin': 'https://www.ystu.ru',
            'Referer': 'https://www.ystu.ru/WPROG/main.php'
        }

    def form_placereq(self): # заказать справку по месту требования
        session = self.s
        h = self.h
        html = session.get('https://www.ystu.ru/WPROG/lk/lkorder.php', headers=h)
        soup = BeautifulSoup(html.text, 'html.parser')
        codeYSTU = soup.find('input', dict(name='codeYSTU'))['value']
        h['Referer'] = 'https://www.ystu.ru/WPROG/lk/lkorder.php'
        jsonp = {
            "codeYSTU": codeYSTU,
            "idord": "0",
            "idordtyp": "3",
            "datt1": '30.08.2024',
            "nameordtyp": "*Справка по месту требования",
            "save": "Сохранить"
        }
        p = session.post('https://www.ystu.ru/WPROG/lk/lkorder_upd.php', data=jsonp, headers=h)
        if 'Добавлено.' in p.content.decode('windows-1251'):
            return True
        else:
            return False
        # return p.content.decode('windows-1251')



    def scholarship(self):
        session = self.s
        h = self.h
        html = session.get('https://www.ystu.ru/WPROG/lk/lkorder.php', headers=h)
        soup = BeautifulSoup(html.text, 'html.parser')
        codeYSTU = soup.find('input', dict(name='codeYSTU'))['value']
        h['Referer'] = 'https://www.ystu.ru/WPROG/lk/lkorder.php'
        jsonp = {
            "codeYSTU": codeYSTU,
            "idord": "0",
            "idordtyp": "5",
            "datt1": '01.07.2024',
            "datt2": '30.09.2024',
            "nameordtyp": "*Справка по месту требования",
            "save": "Сохранить"
        }