from django.views import View
from django.shortcuts import render, redirect


from main.models import User
from main.forms import (
    CreateAccountForm, LogininForm, AddRecipeModelForm, EditProfileForm
)

class CreateAccountWebView(View):
    template_name = 'create_account.html'
    
    def get(self, request):
        form = CreateAccountForm()
        return render(request, self.template_name, {'form': form})

class LogininWebView(View):
    template_name = 'loginin_account.html'
    
    def get(self, request):
        user: User = request.user
        if not user.is_anonymous:
            return redirect('/main/lk_all/get_lk/')

        form = LogininForm()
        return render(request, self.template_name, {'form': form})

class AddRecipeModelWebView(View):
    template_name = 'add_recipe.html'
    
    def get(self, request):
        user: User = request.user
        if user.is_anonymous:
            return redirect('/main/front/loginin/')

        form = AddRecipeModelForm()
        return render(request, self.template_name, {'form': form})

class EditAccountWebView(View):
    template_name = 'edit_account.html'
    
    def get(self, request):
        user: User = request.user
        if user.is_anonymous:
            return redirect('/main/front/loginin/')

        form = EditProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': user.type,
        })
        return render(request, self.template_name, {
            'form': form,
            'email': user.email
        })
