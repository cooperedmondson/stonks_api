from django.urls import path
from . import views

urlpatterns = [
    path("stock/<str:stockQuery>/", views.get_stocks, name="get-stock-info" ),
]
