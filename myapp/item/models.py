#-*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    imageId = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    price = models.CharField(max_length=8)
    gender = models.CharField(max_length=8)
    category = models.CharField(max_length=16)
    ingredients = models.CharField(max_length=128)
    monthlySales = models.IntegerField(default=0)
    oilyRating = models.IntegerField(default=0)
    dryRating = models.IntegerField(default=0)
    sensitiveRating = models.IntegerField(default=0)

    def __str__(self):
        return self.id



class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    oily = models.CharField(max_length=1, default='p')
    dry = models.CharField(max_length=1, default='p')
    sensitive = models.CharField(max_length=1, default='p')

    def __str__(self):
        return self.name


def add_Rating_to_Item(sender, instance, *args, **kwargs):
    if instance.ingredients:
        ingreList=instance.ingredients
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
        instance.ingredients=','+instance.ingredients+','


pre_save.connect(add_Rating_to_Item, sender=Item)
