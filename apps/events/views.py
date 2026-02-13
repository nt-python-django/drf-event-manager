from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters
from .filters import EventFilter
import requests

from .serializers import EventDetailSerializer, EventRegistrationSerailizer
from .models import Event, Registration


class EventCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        serializer = EventDetailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            event_data = serializer.validated_data

            event = Event(**event_data, user=request.user)
            event.save()

            requests.post(
                f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage',
                data={
                    "chat_id": "@testeaknjdfkjasndkjfs",
                    'text': event_data['title']
                }
            )

            return Response(status=status.HTTP_201_CREATED)


class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = EventFilter


class EventRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer


class EventRegistrationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serailizer = EventRegistrationSerailizer(data=request.data)

        if serailizer.is_valid(raise_exception=True):
            data = serailizer.data

            event = Event.objects.filter(pk=data['event']).first()

            if event:
                existing_event = request.user.registrations.filter(event=event).first()
                if not existing_event:
                    event = Registration(user=request.user, event=event)
                    event.save()

                    # agar tg ulangan bolsa notefication yuborish bot orqali
                    if request.user.chat_id:
                        requests.post(
                            f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage',
                            data={
                                "chat_id": request.user.chat_id,
                                'text': 'register boldi'
                            }
                        )

                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            