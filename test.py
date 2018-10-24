import hashlib
from requests_html import HTMLSession
import datetime
from bs4 import BeautifulSoup

days = {0: 'Понедельник: \n', 1: 'Вторник: \n', 2: 'Среда: \n', 3: 'Четверг: \n', 4: 'Пятница: \n'}

def c_parse(login, password):
    pas = password.encode('utf-8')
    pas = str(hashlib.md5(pas).hexdigest())
    session = HTMLSession()
    headers = {'Referer': 'https://www.mos.ru/pgu/ru/application/dogm/journal/'}
    auth_url = "https://mrko.mos.ru/dnevnik/services/index.php"
    auth_req = session.get(auth_url, headers=headers, params={"login": login,
                                                              "password": pas},
                           allow_redirects=False)
    d1 = datetime.datetime.now()
    d1 = datetime.datetime.date(d1)
    d = datetime.datetime.weekday(d1)
    if d == 5 or d == 6 or d == 4:
        try:
            d = datetime.date(d1.year, d1.month, d1.day + 7 - d)
        except Exception:
            d1 = datetime.date(d1.year, d1.month + 1, 1)
            d = datetime.date(d1.year, d1.month + 1, 1 + 7 - datetime.datetime.weekday(d1))
        main_req = session.get("https://mrko.mos.ru/dnevnik/services/dnevnik.php?r=1&first=1&next=" + str(d))
        d = datetime.datetime.weekday(d)
    else:
        main_req = session.get("https://mrko.mos.ru/dnevnik/services/dnevnik.php?r=1&first=1")
    main_req.html.render()
    print(main_req.html.html)
    return
    parsed_html = BeautifulSoup(str(main_req.html), "lxml")
    columns = parsed_html.body.find_all('div', 'b-diary-week__column')
    final_ans = []
    d2 = d + 1
    d = (days[d])[:-3]
    d = d.upper()
    d2 = days[d2][:-3]
    d2 = d2.upper()
    for column in columns:
        date_number = column.find("span", "b-diary-date").text
        date_word = column.find("div", "b-diary-week-head__title").find_all("span")[0].text
        if date_word == d or date_word == d2:
            final_ans.append("<b>" + date_word + "</b> \n" + date_number + "\n \n")
            lessons_table = column.find("div", "b-diary-lessons_table")
            all_lists = lessons_table.find_all("div", "b-dl-table__list")
            for lesson in all_lists:
                lesson_columns = lesson.find_all("div", "b-dl-td_column")
                lesson_number = lesson_columns[0].span.text
                lesson_name = lesson_columns[1].span.text
                if lesson_name == "":
                    pass
                else:
                    lesson_dz = lesson_columns[2].find("div", "b-dl-td-hw-section").span.text
                    lesson_mark = lesson_columns[3].span.text[0:1]
                    final_ans.append(
                        "<b>{0}. {1}</b>. Домашнее задание:\n"
                        "<i>{2}</i>\n"
                        "Оценка за урок: <i>{3}</i>\n\n".format(lesson_number,
                                                                lesson_name,
                                                                lesson_dz,
                                                                lesson_mark))

    return final_ans

print(c_parse("yoyo.aero@yandex.ru", "bumbumsasha2015"))