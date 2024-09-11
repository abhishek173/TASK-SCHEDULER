from django.urls import path
from . views import *

urlpatterns = [
    path('',task_list),
    path('login/',login_page),
    path('logout/',logout_page),
    path('register/',register_page),
    path('create/',task_create),
    path('update/<int:id>',task_update),
    path('task_complete/<int:id>/',task_complete),
    path('delete/<int:id>',task_delete)
]