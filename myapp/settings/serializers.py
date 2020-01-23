from rest_framework import serializers
from .models import Item
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item # 모델 설정
        fields = ('id','imageId','name','price','gender','category','ingredients','monthlySales','oilyRating','dryRating','sensitiveRating') # 필드 설정
