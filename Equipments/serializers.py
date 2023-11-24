from rest_framework import serializers
from django.utils import timezone

from Equipments.models import Equipment,Log,Renting,Returned,Returning

class RequestGetRentingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Renting
        fields= ['id', 'log_id', 'user_id']

class RequestGetReturningSerializer(serializers.ModelSerializer):
    class Meta:
        model= Returning
        fields= '__all__'


class ReturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model= Returned
        fields= '__all__'
class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Renting
        fields= '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.model_name = validated_data.get('model_name', instance.model_name)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.price = validated_data.get('price', instance.price)
        instance.repository = validated_data.get('repository', instance.repository)
        instance.total_stock = validated_data.get('total_stock', instance.total_stock)
        instance.current_stock = validated_data.get('current_stock', instance.current_stock)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        instance.updated_at = timezone.now()

        instance.save()
        return instance
    class Meta:
        model =Equipment
        fields = '__all__'

class LogModifySerializer(serializers.ModelSerializer):
    extend_date = serializers.IntegerField(default=0)

    def update(self, instance, validated_data):
        extend_days = validated_data.get('extend_date', 0)
        instance.return_deadline += timezone.timedelta(days=extend_days)

        instance.save()
        return instance
    class Meta:
        model = Log
        fields= '__all__'
class LogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields= '__all__'

class LogRentAcceptedSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.rent_accepted_date = timezone.now()
        instance.updated_at = timezone.now()
        instance.rent_price = validated_data.get('rent_price', instance.rent_price)
        instance.save()

        #foreign key update
        Renting.objects.filter(log_id=instance).update(rent_accepted_date=instance.rent_accepted_date)

        return instance
    class Meta:
        model= Log
        fields= '__all__'