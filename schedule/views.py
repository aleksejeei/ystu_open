from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from services.parser import ystu
from home.models import ystu_account
from datetime import datetime, timedelta

# Create your views here.

def get_date_from_week(start_date, week_number, day_of_week):
    # Преобразуем строку в объект datetime
    week_number -= 1
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Находим первую дату указанной недели
    first_week_date = start_date + timedelta(weeks=week_number)

    # Вычисляем нужный день (понедельник - это 0)
    target_date = first_week_date + timedelta(days=day_of_week)

    return target_date.isoformat()


@login_required
def index(request):
    start_date_text = '02.09.2024'
    start_date = datetime.strptime(start_date_text, '%d.%m.%Y')
    now_date = datetime.today()
    delta = (now_date - start_date).days
    numberWeek = delta//7+1

    if datetime.today().isoweekday() >= 6:
        numberWeek += 1



    return render(request, 'schedule.html', context={'numberWeek': numberWeek})

@login_required
def get_schedule(request):
    user = request.user
    username = user.username

    ystuAcc = ystu_account.objects.get(username_django=username)
    login = ystuAcc.login
    password = ystuAcc.password
    schedule = ystu.new_schedule(login, password)
    return JsonResponse(data=schedule, safe=True, json_dumps_params={'ensure_ascii': False})