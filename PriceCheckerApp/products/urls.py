from django.urls import path
from . import views
"""
Так мы импортировали функцию path Django
и все views из приложения products
Создали URL-шаблон:
"""

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about_us, name='about'),
    path('search', views.search, name='search'),
    path('product', views.product_view, name='product')
]
'''
Cвязали view под именем index с корневым URL-адресом ('').
Этот шаблон URL будет соответствовать пустой строке.
Для обработчиков URL в Django 'http://127.0.0.1:8000/' не является частью URL.
Этот шаблон скажет Django, что views.index — 
это правильное направление для запроса к нашему веб-сайту по адресу 'http://127.0.0.1:8000/'.

Последняя часть name='home' — это имя URL,
которое будет использовано, чтобы идентифицировать его.
Я буду использовать именованные URL позднее в проекте,
поэтому важно указывать их имена уже сейчас.
Также важно сохранить имена URL-адресов уникальными
и легко запоминающимися.
'''