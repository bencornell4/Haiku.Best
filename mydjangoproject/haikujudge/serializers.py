from rest_framework import serializers
from haikujudge.models import Haiku

class HaikuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Haiku
        fields = ('content', 
                  'author', 
                  'score')