from rest_framework import serializers
from api.models import Template


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        # fields = ('id', 'name', 'description', 'template')
        # extra_kwargs = {'template': {'write_only': True}}
