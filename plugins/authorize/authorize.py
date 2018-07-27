from errbot import BotPlugin, botcmd
from plugins import globals
import requests
import hashlib


class Authorize(BotPlugin):
    """
    Plugin used for authorization on PGU.mos
    to use e-register's timetable, marks, etc.
    """

    @botcmd
    def authorize(self, msg, args):
        login, password = args.split()
        pas = password.encode('utf-8')
        pas = str(hashlib.md5(pas).hexdigest())
        session = requests.Session()
        headers = {'Referer': 'https://www.mos.ru/pgu/ru/application/dogm/journal/'}
        auth_url = "https://mrko.mos.ru/dnevnik/services/index.php"
        auth_req = session.get(auth_url, headers=headers, params={"login": login,
            "password": pas}, allow_redirects=False)

        if auth_req.status_code == 200: # TODO: not a valid check
            print(session.get("https://mrko.mos.ru/dnevnik/services/dnevnik.php", headers=headers).content)
            globals.users[msg.frm] = session
            return 'Авторизован!' # Authorization successful
        return 'Неправильный логин и\или пароль!' # Authorization not successful
