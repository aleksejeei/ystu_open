from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import team, list_members_teams, messages, Tasks
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required
def index(request):
    user_id = User.objects.get(username=request.user).id

    QuerySet_chat_id_user = list_members_teams.objects.filter(user_id=user_id)
    list_chat_id_user = []
    for i in QuerySet_chat_id_user:
        list_chat_id_user.append(i.chat_id)

    chats = []
    for i in list_chat_id_user:
        info = team.objects.get(id=i)
        chats.append([info.name, i])

    content = {
        'chats': chats,
    }
    user = request.user
    testQuery = user.tasks_executed.all()
    test = []
    for i in testQuery:
        dict = {'id': i.id,
                'name': i.nameTask,
                'dueDate': i.dueDate}
        test.append(dict)

    print(list(test))

    #return render(request, 'chats/chats.html', context=content)
    return render(request, 'delegation/main.html', context=content)

@login_required
def view_chats(request):
    user_id = User.objects.get(username=request.user).id
    chat_id = int(request.GET.get('id'))
    QuerySet_chat_id_user = list_members_teams.objects.filter(user_id=user_id, chat_id=chat_id)
    if len(QuerySet_chat_id_user) == 0:
        return redirect('chats')

    messages_QuerySet = messages.objects.filter(chat_id=chat_id)
    chat_name = team.objects.get(id=chat_id).name
    messages_list = []
    for i in messages_QuerySet:
        username = User.objects.get(id=i.user_id).username
        messages_list.append([username, i.content, str(i.date_create).split('.')[0]])
    username = User.objects.get(id=user_id).username
    content = {
        'messages': messages_list,
        'my_username': username,
        'chat_name': chat_name,
        'chat_id': chat_id,
    }

    return render(request, 'chats/chat_in.html', context=content)

# def send_message(request):
#     user_id = User.objects.get(username=request.user).id
#     chat_id = int(request.POST.get('id'))
#     message_text = request.POST.get('message')
#     QuerySet_chat_id_user = list_members_teams.objects.filter(user_id=user_id, chat_id=chat_id)
#     if len(QuerySet_chat_id_user) == 0:
#         return redirect('chats')
#
#    # print(message_text, user_id, chat_id)
#     x = messages(content=message_text, chat_id=chat_id, user_id=user_id)
#     x.save()
#     print(request.headers["Referer"])
#     return redirect(request.headers["Referer"])



