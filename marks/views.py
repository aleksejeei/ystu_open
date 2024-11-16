from django.shortcuts import render, redirect
from home.models import ystu_account, session_data
from services.parser import ystu
from django.contrib.auth.decorators import login_required
from services.settings.session_func import check_sesison
# Create your views here.
@login_required
def index(request):
    check_sesison(request, session_data)
    username = str(request.user)
    db = ystu_account.objects.get(username_django=username)
    login = db.login
    password = db.password

    marks = ystu.get_marks(login, password)
    list_sem = []
    for i in marks:
        list_sem.append(i['semester'])
    list_sem = sorted(list(set(list_sem)))

    content = {
        'list_sem': list_sem,
        'marks': marks
    }

    return render(request, 'marks.html', context=content)