from django.shortcuts import render, redirect
from services.parser import ystu
from home.models import ystu_account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def data_to_text(data):
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
    day = int(data.split('.')[0])
    month = int(data.split('.')[1])
    year = int(data.split('.')[2])
    return f'{day} {dict_month[month]} {year}'
@login_required
def index(request):
    username = str(request.user)
    db = ystu_account.objects.get(username_django=username)
    login = db.login
    password = db.password
    list_state = ystu.get_statements(login, password)
    for i in range(len(list_state)):
        list_state[i]['date'] = data_to_text(list_state[i]['date'])

    content = {
        'info': list_state,
        'count': len(list_state),
        #'csrfmiddlewaretoken': csrf.get_token(request)
    }
    #print(list_state)
    #print()
    return render(request, 'state.html', context=content)

@login_required
def order(request):
    username = str(request.user)
    db = ystu_account.objects.get(username_django=username)
    login = db.login
    password = db.password

    result = request.POST.get('requestName')
    if result == 'place_request':
        print(ystu.form_stateplace(login, password))
    return redirect('statements')
# @login_required
# def del_place(request):
#     username = str(request.user)
#     db = ystu_account.objects.get(username_django=username)
#     login = db.login
#     password = db.password
#
#     number_order = request.POST.get('number_order')
#     print(ystu.delete_state_place(login, password, number_order))
#     return HttpResponse('Test')