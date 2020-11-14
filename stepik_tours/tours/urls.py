from django.urls import path
from tours.views import MainView, DepartureView, TourView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('departure/<str:departure>/', DepartureView.as_view(), name='departures'),
    path('tour/<int:id>/', TourView.as_view(), name='tours'),
    ]
