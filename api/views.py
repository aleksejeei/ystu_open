from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render

class AboutView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        print(user)
        return render(request, 'api.html')

    # def post(self, requset):
    #     form =