from django.urls import path
from . import views
#from rest_framework.urlpatterns import format, format_suffix_paformat_suffix_patterns

urlpatterns = [
    path('add_model/', views.add_model,name="AddModel"),
    path('show_model/', views.show_model,name="ShowModel"),
]



