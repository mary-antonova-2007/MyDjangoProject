from django.contrib import admin
from django.urls import path, include
from .views import main


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('rehearsal/', include('rehearsals.urls')),
]
