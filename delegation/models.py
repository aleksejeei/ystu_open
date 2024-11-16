from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class team(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50, null=False)
    creator = models.ForeignKey(User, related_name='creator_team', on_delete=models.SET_DEFAULT, default='Deleted')
    # member = models.ManyToManyField(User)

class list_members_teams(models.Model):
    def __str__(self):
        return str(self.chat)
    chat = models.ForeignKey(team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default='Deleted', on_delete=models.SET_DEFAULT)

class messages(models.Model):

    chat = models.ForeignKey(team, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, unique=False)
    content = models.TextField(max_length=4000)
    date_create = models.DateTimeField(auto_now=True)

class ConditionTask(models.Model):
    def __str__(self):
        return self.condition
    condition = models.CharField(max_length=30)

class ResultTask(models.Model):
    def __str__(self):
        return self.typeResult
    typeResult = models.CharField(max_length=30)


class Tasks(models.Model):
    def __str__(self):
        return self.taskText

    nameTask = models.CharField(max_length=40)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', default=1)
    dueDate = models.DateTimeField() # срок сдачи
    currentDate = models.DateTimeField(auto_now=True) # дата создания
    taskText = models.TextField()
    executors = models.ManyToManyField(User, related_name='tasks_executed')
    condition = models.ForeignKey(ConditionTask, on_delete=models.CASCADE)
    typeResult = models.ForeignKey(ResultTask, on_delete=models.CASCADE)  #связь с таблицей с типами результатов
    team = models.ForeignKey(team, on_delete=models.CASCADE, default=4, related_name='taskToTeam')