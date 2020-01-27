#-*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# 아이템 테이블
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    imageId = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True)
    price = models.CharField(max_length=8)
    gender = models.CharField(max_length=8)
    category = models.CharField(max_length=16, db_index=True)
    ingredients = models.TextField(max_length=128)
    monthlySales = models.IntegerField(default=0)

    #성분 점수
    oilyRating = models.IntegerField(default=0, db_index=True)
    dryRating = models.IntegerField(default=0, db_index=True)
    sensitiveRating = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.id

# 성분 테이블
class Ingredient(models.Model):
    name = models.CharField(max_length=32, unique=True)
    oily = models.CharField(max_length=1, default='p')
    dry = models.CharField(max_length=1, default='p')
    sensitive = models.CharField(max_length=1, default='p')

    def __str__(self):
        return self.name

# 성분 점수 계산
# 'O' -> +1 / 'X' -> -1 / 나머지 -> 그대로
def add_Rating_to_Item(sender, instance, *args, **kwargs):
    if instance.ingredients:
        ingreList=instance.ingredients

        #Item 테이블의 ingredients를 ','를 기준으로 나눠서 Ingredient테이블에서 검색
        ingredient_List=ingreList.split(',')
        for ingredient in ingredient_List:
            ingr=Ingredient.objects.get(name=ingredient)

            if ingr.oily=='O':
                instance.oilyRating+=1
            elif ingr.oily=='X':
                instance.oilyRating-=1
            else:
                pass

            if ingr.dry == 'O':
                instance.dryRating += 1
            elif ingr.dry == 'X':
                instance.dryRating -= 1
            else:
                pass

            if ingr.sensitive == 'O':
                instance.sensitiveRating += 1
            elif ingr.sensitive == 'X':
                instance.sensitiveRating -= 1
            else:
                pass
        # Item 테이블의 ingredients 앞 뒤에 ',' 추가하여 저장(추후에 검색할때 오류없이 나누기 위해)
        # 예시
        # 원래: "ingredients" : "ab,b,c,d,e" -> 'a' 성분 포함된 것 제거 시 'ab'에 'a'가 포함되어서 제거됨
        # 수정: "ingredients" : ",ab,b,c,d,e," -> ',a,'로 검색하여 'ab' 제거 안됨
        instance.ingredients=','+instance.ingredients+','


pre_save.connect(add_Rating_to_Item, sender=Item)
