from rest_framework import serializers

from Equipments.models import Equipment
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

        instance.save()
        return instance
    class Meta:
        model =Equipment
        fields = '__all__'