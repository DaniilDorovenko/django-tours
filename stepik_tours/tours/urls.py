from django.urls import path

from tours.views import MainView, DepartureView, TourView

# не работает
handler404 = 'tours.views.page_not_found'

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('departure/<str:departure>/',
         DepartureView.as_view(),
         name='departures'),
    path('tour/<int:tour_id>/', TourView.as_view(), name='tours'),
]
