from . import parsers
from . import connect
# import parsers
# import connect


def get_profile(login, password):
    html = connect.get_profile(login, password)
    return parsers.profile(html).full_info()


def get_marks(login, password):
    conn = connect.connect(login, password)
    html = conn.get_marks()
    return parsers.marks(html)

def get_statements(login, password):
    conn = connect.connect(login, password)
    html = conn.get_statements()
    return parsers.statements(html)

def form_stateplace(login, password):
    conn = connect.statements(login, password)
    result = conn.form_placereq()
    return result

def delete_state_place(login, password, number):
    conn = connect.connect(login, password)
    result = conn.delete_placereq(number)
    return result


# получение нового расписания
def new_schedule(login, password):
    conn = connect.connect(login, password)
    html = conn.get_schedule_sem()
    pre_result = parsers.parse_schedule(html)
    result = parsers.finalParse(pre_result)
    return result
