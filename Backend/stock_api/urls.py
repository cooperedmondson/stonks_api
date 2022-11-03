from django.urls import path
from . import views

urlpatterns = [
    path("stock/<str:stockTicker>/", views.get_stocks, name="get-stock-info"),
    path("stonk/<str:stockQuery>/", views.get_stonks, name="get-stock" ),
]
