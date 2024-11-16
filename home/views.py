from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import datetime
#from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import session_data, ystu_account
from settings.models import is_beta
from services.parser import ystu
from services.settings.session_func import check_sesison
from services.settings.autoremove_avatars import deletePhotos

def ystu_w_info(info, username, login, password):
    date_birthday = datetime.datetime.strptime(info['birthday'], '%d.%m.%Y')
    x = ystu_account(username_django=username,
                     login=login,
                     password=password,
                     full_name=info['full_name'],
                     group=info['group'],
                     address=info['address'],
                     ystu_email=info['ystu_email'],
                     private_email=info['private_email'],
                     phone=info['phone'],
                     birthday=date_birthday,
                     numlib=info['numlib'],
                     faculty=info['faculty'],
                     direction_name=info['direction_name'],
                     direction_code=info['direction_code'])
    x.save()


# Create your views here.
@login_required
def index(request):
    check_sesison(request, session_data)

    username = request.user

    superuser = str(username.is_superuser)

    if len(ystu_account.objects.filter(username_django=str(username))) == 0:
        return render(request, 'ystu_connect.html')

    user_id = username.id
    try:
        beta = str(is_beta.objects.get(user=user_id))
    except:
        beta='False'


    info = ystu_account.objects.get(username_django=username)
    content = {
        'full_name': info.full_name,
        'group': info.group,
        'direction_name': info.direction_name,
        'username': username,
        'beta': beta,
        'superuser': superuser,
        'file': info.avatar_image.url
    }

    #print(info.avatar_image.url)
    deletePhotos()

    return render(request, 'home.html', context=content)

@login_required
def ystu_connect(request):
    check_sesison(request, session_data)

    login = request.POST.get('login')
    password = request.POST.get('password')
    username = request.user

    try:
        info = ystu.get_profile(login, password)
    except:
        return render(request, 'ystu_connect.html')

    user = User.objects.get(username=username)
    user.first_name = info['full_name'].split()[1]
    user.last_name = info['full_name'].split()[0]
    user.save()

    ystu_w_info(info, user, login, password)
    return redirect('home')



class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'


def registration(request):
    if str(request.user) != 'AnonymousUser':
        return redirect('home')
    return render(request, 'registration/reg.html')

def create_account(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    login_ystu = request.POST.get('username-ystu')
    password_ystu = request.POST.get('password-ystu')



    try:
        info = ystu.get_profile(login_ystu, password_ystu)
    except:
        return HttpResponse('Ошибка, неверный логин или пароль от портала ЯГТУ')

    user = User.objects.create_user(username=username, password=password)

    user.first_name = info['full_name'].split()[1]
    user.last_name = info['full_name'].split()[0]
    user.save()

    ystu_w_info(info, user, login_ystu, password_ystu)

    return redirect('login')



