from django.shortcuts import render, HttpResponse, redirect
# from registration.models import profile, profile_info
from home.models import ystu_account, session_data
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from services.settings.session_func import check_sesison
# Create your views here.


def get_user_sessions(user):
    # Получаем все сессии
    sessions = Session.objects.all()
    user_sessions = []

    for session in sessions:
        # Десериализуем данные сессии
        data = session.get_decoded()

        # Проверяем, соответствует ли пользователь
        if data.get('_auth_user_id') == str(user.id):
            user_sessions.append(session)

    return user_sessions


@login_required
def index(request):
    check_sesison(request, session_data)
    return render(request, 'settings.html')

@login_required
def sessions(request):
    check_sesison(request, session_data)

    key_s = request.session.session_key
    user = request.user

    queryset_sessions = get_user_sessions(user)
    list_sessions = []
    for i in queryset_sessions:
        list_sessions.append(str(i))
    list_html = []
    for i in list_sessions:
        try:
            if i == key_s:
                objectq = session_data.objects.get(session_key=key_s)
                current_session = [objectq.user_agent, str(objectq.data_first_auth).split('.')[0], key_s]
            else:
                objectq = session_data.objects.get(session_key=i)
                list_html.append([objectq.user_agent, str(objectq.data_first_auth).split('.')[0], i])
        except:
            pass
    #print(current_session, list_html)

    content = {
        'list_session': list_html,
        'current_session': current_session,
        'username': user,
    }

    return render(request, 'session.html', context=content)

@login_required
def del_session(request):
    key_s = request.POST.get('id')
    print(key_s)
    session_data.objects.get(session_key=key_s).delete()
    Session.objects.get(session_key=key_s).delete()
    return redirect('session')
@login_required
def view_profile(request):
    check_sesison(request, session_data)
    username = str(request.user)
    try:
        info = ystu_account.objects.get(username_django=username)
    except:
        return redirect(request.headers["Referer"])

    content = {
        'username': username,
        'login': info.login,
        'full_name': info.full_name,
        'group': info.group,
        'email': info.ystu_email,
        'faculty': info.faculty,
        'direction_name': info.direction_name
    }

    return render(request, 'profile_set.html', context=content)
@login_required
def ystu_disconnect(request):
    username = request.user
    ystu_account.objects.get(username_django=username).delete()
    return redirect('home')