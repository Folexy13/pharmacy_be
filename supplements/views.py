from django.http import JsonResponse
from .models import Category, SubCategory


def get_categories(request):
    main_category_id = request.GET.get('main_category')
    categories = Category.objects.filter(main_category_id=main_category_id)
    data = {'categories': [{'id': c.id, 'name': c.name} for c in categories]}
    return JsonResponse(data)


def get_subcategories(request):
    category_ids = request.GET.get('categories', '').split(',')
    subcategories = SubCategory.objects.filter(category_id__in=category_ids)
    data = {'subcategories': [{'id': s.id, 'name': s.name} for s in subcategories]}
    return JsonResponse(data)
