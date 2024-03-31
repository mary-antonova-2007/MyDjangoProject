from django.urls import path
from . import views

urlpatterns = [
    path('available-dates/', views.available_dates, name='available_dates'),
    path('data-by-date/<int:day>/<int:month>/<int:year>/', views.data_by_date, name='data_by_date'),
    path('rehearsal-rooms/', views.rehearsal_rooms, name='rehearsal_rooms'),
    path('rehearsal-info/<int:day>/<int:month>/<int:year>/', views.rehearsal_info, name='rehearsal_info'),
]