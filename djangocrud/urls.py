from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.addTable, name='add_table'),
    path('edit/<str:id>', views.editTable, name='edit_table'),
    path('delete/<str:id>', views.deleteRecord, name='delete_record'),
]
