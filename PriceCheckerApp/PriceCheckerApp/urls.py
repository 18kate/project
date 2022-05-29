from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls'))
]
"""
Django теперь будет перенаправлять все запросы 'http://127.0.0.1:8000/'
к products.urls и искать там дальнейшие инструкции.
"""