import requests

from django.views import View
from django.shortcuts import render

from main.forms import CreateAccountForm

class CreateAccountWebView(View):
    template_name = 'create_account.html'
    
    def get(self, request):
        form = CreateAccountForm()
        return render(request, self.template_name, {'form': form})
    