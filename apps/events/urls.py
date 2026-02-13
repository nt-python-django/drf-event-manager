from django.urls import path

from .views import EventCreateView, EventListView, EventRetrieveView, EventRegistrationView


urlpatterns = [
    path('', EventCreateView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='events-list'),
    path('<int:pk>/', EventRetrieveView.as_view(), name='event-get'),
    path('registeration/', EventRegistrationView.as_view(), name='event-register'),
]