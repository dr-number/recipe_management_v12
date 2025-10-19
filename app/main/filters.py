from django.contrib import admin

class TimeCookingFilter(admin.SimpleListFilter):
    title = 'Время приготовления'
    parameter_name = 'time_cooking'
    
    def lookups(self, request, model_admin):
        return [
            ('fast', 'Быстрые (< 30 мин)'),
            ('medium', 'Средние (30-60 мин)'),
            ('long', 'Долгие (> 60 мин)'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'fast':
            return queryset.filter(time_cooking__lt='00:30:00')
        if self.value() == 'medium':
            return queryset.filter(time_cooking__range=('00:30:00', '01:00:00'))
        if self.value() == 'long':
            return queryset.filter(time_cooking__gt='01:00:00')