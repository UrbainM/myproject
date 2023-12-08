# myproject/urls.py
from django.contrib import admin
from django.urls import include, path
from myapp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('myapp/', include('myapp.urls')),
]
