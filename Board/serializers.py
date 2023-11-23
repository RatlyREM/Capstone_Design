from rest_framework import serializers
from django.utils import timezone
from Board.models import BoardModel

class BoardSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.field = validated_data.get('field', instance.field)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.updated_at = timezone.now()

        instance.save()
        return instance

    class Meta:
        model = BoardModel
        fields = '__all__'