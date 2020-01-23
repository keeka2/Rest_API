from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from myapp.item.serializers import ItemSerializer
from myapp.item.serializers import ItemDetailSerializer
from myapp.item.serializers import ItemRecommendSerializer
from myapp.item.models import Item
from myapp.item.models import Ingredient
from django.db.models.functions import Length

def index(request):
    return render(request, 'index.html', {})

@csrf_exempt
def ProductList(request):
    if request.method == 'GET':
        query_set = Item.objects.all()

        skin_type = request.GET.get('skin_type', None)
        category = request.GET.get('category', None)
        page = request.GET.get('page', None)
        exclude_ingredient = request.GET.get('exclude_ingredient', None)
        include_ingredient = request.GET.get('include_ingredient', None)

        #category 검색 시 결과가 없다면 에러
        if category is not None:
            query_set = query_set.filter(category=category)
            if query_set.count()==0:
                return JsonResponse({'message': 'category Not Found'}, safe=False)

        #exclude_ingredient 검색 시 ingredient 테이블에 없는 성분일 시 에러
        if exclude_ingredient is not None:
            ex_ingredient=exclude_ingredient.split(',')
            for temp_ingredient in ex_ingredient:
                if Ingredient.objects.filter(name=temp_ingredient).exists() == False:
                    return JsonResponse({'message': 'ingredient ->' +temp_ingredient+ '<- Not Found'}, safe=False)
                query_set = query_set.exclude(ingredients__contains=','+temp_ingredient+',')

        #include_ingredient 검색 시 ingredient 테이블에 없는 성분일 시 에러
        if include_ingredient is not None:
            in_ingredient=include_ingredient.split(',')
            for temp_ingredient in in_ingredient:
                if Ingredient.objects.filter(name=temp_ingredient).exists() == False:
                    return JsonResponse({'message': 'ingredient ->' +temp_ingredient+ '<- Not Found'}, safe=False)
                query_set = query_set.filter(ingredients__contains=','+temp_ingredient+',')

        #skin_type 입력이 없으면 에러
        if skin_type is not None:
            # skin_type이 oily, dry, sensitive가 아닐 시 에러
            if skin_type=='oily' or skin_type=='dry' or skin_type=='sensitive':
                pass
            else:
                return JsonResponse({'message': 'Wrong skin_type Input'}, safe=False)
            #skin_type 변수가 검색한 skin_type에 따라서 '-oilyRating' or '-dryRating' or '-sensitiveRating'으로 바뀜
            skin_type = '-' + skin_type + 'Rating'
            #검색한 성분점수 내림차순, 가격 오름차순으로 데이터 받아오기
            #price가 string형태이기 때문에 int로 바꿔서 오름차순
            query_set = query_set.extra({'priceInt': "CAST(price as UNSIGNED)"}).order_by(skin_type,'priceInt')
        else:
            return JsonResponse({'message': 'skin_type Not Found'}, safe=False)

        #지금까지 queryset 개수
        total=query_set.count()

        #총 데이터 수로 가능한 최대 페이지 구하기(total=450이면 max_Page=9 / total=451이면 max_Page=10)
        if total%50==0:
            max_Page=int(total/50)
        else:
            max_Page=int(total/50)+1

        #page 검색 시 데이터의 인덱스 구하기(page=1 이면 start=0, end=49)
        if page is not None:
            #검색한 page가 max_page보다 크면 에러
            if int(page)<=max_Page:
                start=(int(page)-1)*50
                end=(int(page)*50)
                if end>total:
                    end=total
                query_set=query_set[start:end]
            else:
                return JsonResponse({'message': 'Page is between 1~'+max_page}, safe=False)

        serializer = ItemSerializer(query_set,many=True)

        #ImageID로 ImageUrl 생성
        # for i in serializer.data:
        #     i['imageUrl'] = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/" + i['imageId'] + ".jpg"
        #     n=len(i['ingredients'])
        #     i['ingredients'] = i['ingredients'][1:n-1]
        #     del i['imageId']
        return JsonResponse(serializer.data, safe=False, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def ProductDetail(request, pk):
    obj=Item.objects.get(pk=pk)
    #검색한 id(pk)의 category 저장
    category=Item.objects.values_list('category',flat=True).get(pk=pk)

    if request.method == 'GET':
        serializer = ItemDetailSerializer(obj)
        detail_Pk=serializer.data
        detail_Pk['imageUrl']="https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/"+detail_Pk['imageId']+".jpg"
        del detail_Pk['imageId']

        skin_type = request.GET.get('skin_type', None)
        query_set = Item.objects.all()

        #위와 동일
        #추천 리스트 결과에서는 이미 검색한 id(pk) 제외
        query_set = query_set.exclude(pk=pk)
        if category:
            query_set = query_set.filter(category=category)

        # skin_type 입력이 없으면 에러
        if skin_type is not None:
            # skin_type이 oily, dry, sensitive가 아닐 시 에러
            if skin_type == 'oily' or skin_type == 'dry' or skin_type == 'sensitive':
                pass
            else:
                return JsonResponse({'message': 'Wrong skin_type Input'}, safe=False)
            skin_type = '-' + skin_type + 'Rating'

            #검색한 결과에 대해 상위 3개만 저장
            query_set = query_set.extra({'priceInt': "CAST(price as UNSIGNED)"}).order_by(skin_type,'priceInt')[:3]
        else:
            return JsonResponse({'message': 'skin_type Not Found'}, safe=False)

        serializer2 = ItemRecommendSerializer(query_set, many=True)
        All=serializer2.data
        # ImageID로 ImageUrl 생성
        for i in All:
            i['imageUrl']= "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"+i['imageId']+".jpg"
            del i['imageId']


        #추천상품 리스트 앞에 pk검색 결과 붙이기
        All.insert(0,detail_Pk)

        return JsonResponse(All, safe=False, json_dumps_params = {'ensure_ascii': False})

