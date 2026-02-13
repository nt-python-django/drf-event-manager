from rest_framework import serializers

from .models import Event


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['user']


class EventRegistrationSerailizer(serializers.Serializer):
    event = serializers.IntegerField()

    def validate_event(self, value):
        if value < 0:
            raise serializers.ValidationError('event 0 dan katta bolsin')
        return value
    