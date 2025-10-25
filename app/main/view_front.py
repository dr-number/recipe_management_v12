import requests

from django.views import View
from django.shortcuts import render

from main.forms import CreateAccountForm

class CreateAccountWebView(View):
    template_name = 'create_account.html'
    
    def get(self, request):
        form = CreateAccountForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CreateAccountForm(request.POST)
        
        if form.is_valid():
            # Подготовка данных для API
            api_data = {
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'password': form.cleaned_data['password'],
                'password2': form.cleaned_data['password2'],
                'type': form.cleaned_data['type']
            }
            
            try:
                # Отправка запроса к вашему API
                api_url = 'http://your-domain/api/create-account/'  # замените на ваш URL
                response = requests.post(
                    api_url,
                    json=api_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    # Успешная регистрация
                    return render(request, 'registration_success.html', {
                        'success': True,
                        'response_data': response.json()
                    })
                else:
                    # Ошибка от API
                    error_data = response.json()
                    return render(request, self.template_name, {
                        'form': form,
                        'api_errors': error_data
                    })
                    
            except requests.RequestException as e:
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'Ошибка соединения с сервером'
                })
        
        return render(request, self.template_name, {'form': form})