from django.contrib import admin
from django.db.models import Avg, Count
from django.db import models

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

class RatingFilter(admin.SimpleListFilter):
    title = 'Рейтинг'
    parameter_name = 'rating'
    
    def lookups(self, request, model_admin):
        return (
            ('0', 'Без рейтинга'),
            ('1', '1+ звезда'),
            ('2', '2+ звезды'),
            ('3', '3+ звезды'),
            ('4', '4+ звезды'),
            ('5', '5 звезд'),
        )
    
    def queryset(self, request, queryset):
        _value = self.value()
        if _value == '0':
            return queryset.annotate(
                rating_count=Count('comment')
            ).filter(rating_count=0)
        
        elif _value:
            min_rating = float(_value)
            return queryset.annotate(
                avg_rating=Avg('comment__raiting')
            ).filter(avg_rating__gte=min_rating)
        
        return queryset