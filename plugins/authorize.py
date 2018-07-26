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
        login, password = msg.split()
        pas = password.encode('utf-8')
        pas = str(hashlib.md5(pas).hexdigest())
        session = requests.Session()
        headers = {'Referer': 'https://www.mos.ru/pgu/ru/application/dogm/journal/'}
        auth_url = "https://mrko.mos.ru/dnevnik/services/index.php"
        auth_req = session.get(auth_url, headers=headers, params={"login": login,
            "password": pas}, allow_redirects=False)
        globals.users[msg.frm] = session
        return 'Authorized!'
