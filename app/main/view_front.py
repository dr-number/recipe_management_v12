from django.views import View
from django.shortcuts import render

from main.forms import CreateAccountForm, LogininForm, AddRecipeModelForm

class CreateAccountWebView(View):
    template_name = 'create_account.html'
    
    def get(self, request):
        form = CreateAccountForm()
        return render(request, self.template_name, {'form': form})

class LogininWebView(View):
    template_name = 'loginin_account.html'
    
    def get(self, request):
        form = LogininForm()
        return render(request, self.template_name, {'form': form})

class AddRecipeModelWebView(View):
    template_name = 'add_recipe.html'
    
    def get(self, request):
        form = AddRecipeModelForm()
        return render(request, self.template_name, {'form': form})
