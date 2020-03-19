from rest_framework import serializers
from my_portal.tooling import models

class ToolConditionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ToolCondition
        fields = '__all__'

class ToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tool
        fields = '__all__'