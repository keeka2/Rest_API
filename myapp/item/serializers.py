from rest_framework import serializers
from .models import Item
class ItemSerializer(serializers.ModelSerializer):
    imgUrl=serializers.SerializerMethodField('get_imageId')

    class Meta:
        model = Item # 모델 설정
        fields = ('id','imgUrl','name','price','gender','category','ingredients','monthlySales','oilyRating','dryRating','sensitiveRating') # 필드 설정
    def get_imageId(self, obj):
        return "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/" + obj.imageId + ".jpg"


class ItemDetailSerializer(serializers.ModelSerializer):
    imgUrl=serializers.SerializerMethodField('get_imageId')
    class Meta:
        model = Item # 모델 설정
        fields = ('id','imageId','name','price','gender','category','ingredients','monthlySales','oilyRating','dryRating','sensitiveRating') # 필드 설정
    def get_imageId(self, obj):
        return "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/" + obj.imageId + ".jpg"

class ItemRecommendSerializer(serializers.ModelSerializer):
    imgUrl=serializers.SerializerMethodField('get_imageId')
    class Meta:
        model = Item # 모델 설정
        fields = ('id','imageId','name','price','category','oilyRating','dryRating','sensitiveRating') # 필드 설정
    def get_imageId(self, obj):
        return "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/" + obj.imageId + ".jpg"