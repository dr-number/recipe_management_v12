from django.contrib import admin
from django.db.models import Avg, Q, Count, F

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
            ('no_rating', 'Без рейтинга'),
            ('1', '1 звезда (1.00-1.99)'),
            ('2', '2 звезды (2.00-2.99)'),
            ('3', '3 звезды (3.00-3.99)'),
            ('4', '4 звезды (4.00-4.99)'),
            ('5', '5 звезд (5.00)'),
        )
    
    def queryset(self, request, queryset):
        value = self.value()
        
        if value == 'no_rating':
            return queryset.annotate(
                avg_rating=Avg(
                    'comment__raiting',
                    filter=~Q(comment__user=F('user'))
                )
            ).filter(
                Q(avg_rating__isnull=True) | Q(avg_rating=0)
            )
        
        elif value:
            rating_ranges = {
                '1': (1.00, 1.99),
                '2': (2.00, 2.99),
                '3': (3.00, 3.99),
                '4': (4.00, 4.99),
                '5': (5.00, 5.00),
            }
            
            min_rating, max_rating = rating_ranges[value]
            
            return queryset.annotate(
                avg_rating=Avg(
                    'comment__raiting',
                    filter=~Q(comment__user=F('user'))  # Исключаем комментарии автора
                ),
                comment_count=Count(
                    'comment',
                    filter=~Q(comment__user=F('user'))  # Также исключаем из подсчета комментариев
                )
            ).filter(
                avg_rating__gte=min_rating,
                avg_rating__lte=max_rating,
                avg_rating__isnull=False
            ).exclude(comment_count=0)
        
        return queryset
