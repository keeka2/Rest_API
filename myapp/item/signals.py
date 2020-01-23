from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Item

@receiver(pre_save, sender=Item)
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
            elif ingr.oily == 'X':
                instance.sensitiveRating -= 1
            else:
                pass
