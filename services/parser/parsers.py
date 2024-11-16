# import requests
import json
from bs4 import BeautifulSoup
#import datetime
from datetime import timedelta, datetime


def time_range4(timerange, infoLess='лек.*'):
    if timerange == '08:30-...10ч':
        return '08:30-10:00'

    #if '4ч' not in timerange:
    if '...' not in timerange and 'ч' not in timerange:
        return timerange

    if 'ч' not in infoLess:
        hours = 2
        #print(timerange)
        #print(hours)
    elif 'ч' in infoLess:
        hours = int(infoLess.split()[1][:-1])
        #print(hours)
    else:

        hours = 2
        #print(hours)

    time1 = timerange.split('-')[0]
    time1 = datetime.strptime(time1, '%H:%M')
   # time2 = time1 + timedelta(minutes=47.5 * 4)

    if time1.strftime('%H:%M') == '15:40' and hours == 4:
        time2 = time1 + timedelta(minutes=45*hours+20)
        return f'{time1.strftime("%H:%M")}-{time2.strftime("%H:%M")}'

    elif time1.strftime('%H:%M') == '12:20' and hours == 4:
        time2 = time1 + timedelta(minutes=45*hours+10)
        return f'{time1.strftime("%H:%M")}-{time2.strftime("%H:%M")}'

    time2 = time1 + timedelta(minutes=45 * hours + hours / 2 * 5)
    #return f'{str(time1).split()[1][0:5]}-{str(time2).split()[1][0:5]}'
    #print(time1)
    return f'{time1.strftime("%H:%M")}-{time2.strftime("%H:%M")}'

def type_lesson(value):
    if 'пр.з' in value:
        return 'Практическое занятие'
    elif 'лек' in value:
        return 'Лекция'
    elif 'лаб' in value:
        return 'Лабораторная работа'
    else:
        #print(value)
        return value

def type_for_html(value):
    if 'пр.з' in value:
        return 'practice'
    elif 'лек' in value:
        return 'lecture'
    elif 'лаб' in value:
        return 'lab'
    else:
        return 'none'

class profile:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def name(self):
        name = self.soup.h1.text
        return name

    def group(self):
        group_name = self.soup.find_all('table')[1].find_all('tr')[3].find_all('td')[1].text.strip()
        return group_name

    def address(self):  # получение адреса со страницы аккаунта
        address = self.soup.find_all('table')[3].find_all('tr')[4].find_all('font')[0].text
        return address

    def ystu_email(self):
        email = self.soup.find_all('table')[3].find_all('td')[5].find('font').text.split()
        return email[1]

    def private_email(self):
        email = self.soup.find_all('table')[3].find_all('td')[5].find('font').text.split()
        return email[0]

    def phone(self):  # номер телефона
        text = str(self.soup.find_all('td'))
        text = text.replace('<td><font size="-1">', 'address_ystu')
        text = text.replace('</font></td>', 'address_ystu')
        text = text.split('address_ystu')
        return text[5].strip()

    def birthday(self):
        birthday = self.soup.find_all('table')[3].find_all('tr')[3].find('td').text.strip()
        return birthday

    def numlib(self):
        numlib = self.soup.find_all('table')[3].find_all('tr')[8].find_all('td')[1].find('font').text.split()[0]
        return numlib

    def faculty_name(self):
        faculty_name = self.soup.find_all('table')[1].find_all('tr')[2].find_all('td')[1].text.strip()
        return faculty_name

    def direction_name(self):
        direction_name = self.soup.find_all('table')[1].find_all('tr')[4].find_all('td')[1].text.split('-')
        return direction_name[1].strip()

    def direction_code(self):
        direction_name = self.soup.find_all('table')[1].find_all('tr')[4].find_all('td')[1].text.split('-')
        return direction_name[0].strip()

    def full_info(self):
        info = {
            "full_name": self.name(),  # ФИО
            'group': self.group(),  # номер группы
            'address': self.address(),  # адрес регистрации
            'ystu_email': self.ystu_email(),  # электронная почта вуза и обычная
            'private_email': self.private_email(),
            'phone': self.phone(),  # номер телефона
            'birthday': self.birthday(),  # дата рождения
            'numlib': self.numlib(),  # номер читательского билета
            'faculty': self.faculty_name(),
            'direction_name': self.direction_name(),
            'direction_code': self.direction_code(),
        }
        #return json.dumps(info, ensure_ascii=False)
        return info


def marks(html): # парсинг оценок
    soup = BeautifulSoup(html, 'html.parser')
    rows = str(soup.find('table', class_='sortb', id='tab1'))
    rows = rows.replace('<td>Оценка</td></tr></thead>', '<tbody>')
    rows = rows.replace('</table>', '</tbody>') + '</table>'
    soup = BeautifulSoup(rows, 'html.parser')
    rows = soup.find('tbody').find_all('tr')

    marks = []
    for row in rows:
        columns = row.find_all('td')
        #data_list = [columns[1].text.strip(), columns[2].text.strip(), columns[3].text.strip(), columns[4].text.strip(), columns[5].text.strip(), columns[6].text.strip(), columns[7].text.strip()]

        data_dict = {
            'course': columns[1].text.strip(),
            'semester': columns[2].text.strip(),
            'subject': columns[3].text.strip(),
            'type_exam': columns[4].text.strip(),
            'zed': columns[5].text.strip(),
            'mark': columns[6].text.strip(),
            'mark_word': columns[7].text.strip()
        }

        #marks.append(data_list)
        marks.append(data_dict)
    return marks
    # return json.dumps(marks, ensure_ascii=False)


def statements(html): # парсинг данных о заявках
    #html = open('test.html').read()
    html_text = BeautifulSoup(html, 'html.parser')
    result = html_text.find_all('table')[0].find_all('tr')
    statements = []
    for i in range(1, len(result)):
        s = result[i].find_all('td')
        # state = [s[0].text.strip(), s[1].text.strip(), s[2].text.strip(), s[4].text.strip(), s[5]['title'].strip()]

        state_dict = {'number': s[0].text.strip(),
                      'date': s[1].text.strip(),
                      'type': s[2].text.strip(),
                      'department': s[4].text.strip(),
                      'status': s[5]['title'].strip()
                      }

        statements.append(state_dict)
    # return json.dumps(statements, ensure_ascii=False)
    return statements


# новый парсинг расписания на весь семестр
def get_date_from_week(start_date, week_number, day_of_week):
    # Преобразуем строку в объект datetime
    week_number -= 1
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Находим первую дату указанной недели
    first_week_date = start_date + timedelta(weeks=week_number)

    # Вычисляем нужный день (понедельник - это 0)
    target_date = first_week_date + timedelta(days=day_of_week)

    return target_date.isoformat()

def dateToText(string):
    date = string.split('T')[0]
    day = date.split('-')[2]
    month = date.split('-')[1]
    dict_month = {
        1: 'Января',
        2: "Февраля",
        3: "Марта",
        4: "Апреля",
        5: "Мая",
        6: "Июня",
        7: "Июля",
        8: "Августа",
        9: "Сентября",
        10: "Октября",
        11: "Ноября",
        12: "Декабря"
    }
    return f'{day} {dict_month[int(month)]}'


def sort_week(string):
    weeks_s = string
    if 'н/н' in weeks_s:
        n = 1 # по нечетным неделям
        weeks_s = weeks_s.replace('н/н', '')
    elif 'ч/н' in weeks_s:
        n = 2 # по четным неделям
        weeks_s = weeks_s.replace('ч/н', '')
    else:
        n = 0
    list_week = []

    if "дистант" in weeks_s:
        isDistant = True
    else:
        isDistant = False

    if '(' in weeks_s:
        weeks_s = weeks_s.split('(')[0].strip()
        #print(weeks_s)

    for week in weeks_s.split(','):
        week = week.strip()

        if '-' not in week:
            if week[-1] == 'н':
                list_week.append(int(week[:-1]))
            else:
                try:
                    list_week.append(int(week))
                except:
                    pass
                   # print(weeks_s.split(','))

        elif '-' in week and 'н' not in week and n == 0:
            num1 = int(week.split('-')[0])
            num2 = int(week.split('-')[1])
            for w in range(num1, num2+1):
                list_week.append(w)
        elif '-' in week and 'н' in week and n == 0:
            num1 = int(week.split('-')[0])
            num2 = int(week.split('-')[1][:-1])
            for w in range(num1, num2+1):
                list_week.append(w)
        elif '-' in week and 'н' in week and (n == 1 or n == 2):
            num1 = int(week.split('-')[0])
            num2 = int(week.split('-')[1][:-1])
            for w in range(num1, num2+1, 2):
                list_week.append(w)
        else:
            print('Error')

    return (list_week, isDistant)


def days_week(html):
    schedule_soup = BeautifulSoup(html, 'html.parser')
    day_week = schedule_soup.find_all('center')
    list_days = []
    for day in range(2, len(day_week)):
        dict_days = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6
        }
        list_days.append(dict_days[day_week[day].text])
    #print(list_days)
    return list_days



def parse_schedule(html):
    schedule_soup = BeautifulSoup(html, 'html.parser') # создаем соуп для bs4
    days = schedule_soup.find_all('table') # ищем все таблицы с расписанием по каждому дню
    listWeekDays = [] # список для
    for day in range(2, len(days)-1):
        daysLessonsList = []
        lessons = days[day].find_all('tr')
        for x in range(1, len(lessons)):
            lessons_data = lessons[x].find_all('td')
            if len(lessons_data) == 6:
                originalTimeTitle = lessons_data[0].text.strip()
                info = lessons_data[1].text.strip()
                info = sort_week(info)
                isDistant = info[1]
                weeks = info[0]
                lessonName = lessons_data[2].text.strip()
                typeLesson = lessons_data[3].text.strip()
                auditoryName = lessons_data[4].text.strip()
                teacherName = lessons_data[5].text.strip()
            else:
                originalTimeTitle = lessons[x - 1].find_all('td')[0].text.strip()
                # orig_weeks = lessons_data[0].text.strip()
                info = lessons_data[0].text.strip()
                info = sort_week(info)
                weeks = info[0]
                isDistant = info[1]
                lessonName = lessons_data[1].text.strip()
                typeLesson = lessons_data[2].text.strip()
                auditoryName = lessons_data[3].text.strip()
                teacherName = lessons_data[4].text.strip()
                if 'н' in originalTimeTitle:
                    for i in range(1, 10):
                        orig = lessons[x - i].find_all('td')[0].text.strip()
                        if 'н' not in orig:
                            originalTimeTitle = orig
                            break

            lesson = {
                'originalTimeTitle': originalTimeTitle,
                'weeks': weeks,
                'lessonName': lessonName,
                'typeLesson': typeLesson,
                'auditoryName': auditoryName,
                'isDistant': isDistant,
                'teacherName': teacherName
            }
            #print(lesson)
            daysLessonsList.append(lesson)
        #print(daysLessonsList)
        listWeekDays.append(daysLessonsList)
        #print('----')
    #print(listWeekDays)
    days_weeks = days_week(html)
    postList = {}
    for numberDay in range(len(days_weeks)):
        postList[days_weeks[numberDay]] = listWeekDays[numberDay]
    return postList



def finalParse(parse):
    diction = {}
    days_text = ['Пн', 'Вт', 'Ср', 'Чт', "Пт", "Сб", "Вс"]

    diction['items'] = []
    for week in range(0, 35):
        days = []
        for day in parse.keys():
            lessons = []
            data = get_date_from_week('2024-09-02', week, day)
            info = {
                'type': day,
                'weekNumber': week,
                'dayText': days_text[day],
                'data': data,
                'dateText': dateToText(data)
                }
            for z in parse[day]:
                if week in z['weeks']:
                    originalTimeTitle = z['originalTimeTitle']
                    number = int(originalTimeTitle.split('.')[0])
                    timeRange = originalTimeTitle.split('. ')[1]
                    typeOfActivity = z['typeLesson']
                    timeRange = time_range4(timeRange, typeOfActivity)
                    test = {
                            'number': number,
                            'timeRange': timeRange,
                            'originalTimeTitle': originalTimeTitle,
                            'lessonName': z['lessonName'],
                            'isDistant': z['isDistant'],
                            'typeLessonOrig': typeOfActivity,
                            'htmlTypeLesson': type_for_html(typeOfActivity),
                            'textTypeLesson': type_lesson(typeOfActivity),
                            'auditoryName': z['auditoryName'],
                            'teacherName': z['teacherName'],
                            }
                    lessons.append(test)
            if len(lessons) != 0:
                infoLessons = {
                    'info': info,
                    'lessons': lessons,
                }
                days.append(infoLessons)
        if len(days) != 0:
            items = {
                'number': week,
                'days': days
            }
            diction['items'].append(items)
    #print(json.dumps(diction, ensure_ascii=False))
    return diction