#from home.models import session_data


def check_sesison(request, session_data):
    user_agent = request.META['HTTP_USER_AGENT']
    key_s = request.session.session_key
    queryset_session_data = session_data.objects.all()
    list_session_data = []
    for i in range(len(queryset_session_data)):
        list_session_data.append(str(queryset_session_data[i]))
    if key_s not in list_session_data:
        session_data.objects.create(session_key=key_s, user_agent=user_agent)