
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from monitoring.repositories.analytics import AnalyticsRepository


analytics_repo = AnalyticsRepository()


@api_view(['GET'])
@permission_classes([AllowAny])  
def avg_prices_by_product_type_view(request):
    try:
        data = list(analytics_repo.get_avg_prices_by_product_type())
        
        # Конвертуємо Decimal в float
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        statistics = {
            'total_product_types': len(data),
            'avg_regular_price_overall': sum(item['avg_regular_price'] for item in data) / len(data),
            'avg_promo_price_overall': sum(item.get('avg_promo_price', 0) or 0 for item in data) / len(data),
            'total_products': sum(item['product_count'] for item in data),
            'max_avg_regular_price': max(item['avg_regular_price'] for item in data),
            'min_avg_regular_price': min(item['avg_regular_price'] for item in data)
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def store_statistics_by_city_view(request):
    try:
        queryset = analytics_repo.get_store_statistics_by_city()
        
        city_filter = request.GET.get('city', None)
        if city_filter:
            queryset = queryset.filter(city__icontains=city_filter)
        
        data = list(queryset)
        
        # Конвертуємо Decimal в float
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        total_stores = sum(item['store_count'] for item in data)
        total_products = sum(item['total_products'] for item in data)
        
        statistics = {
            'total_cities': len(data),
            'total_stores': total_stores,
            'total_products': total_products,
            'avg_products_per_store': total_products / total_stores if total_stores > 0 else 0,
            'avg_price_overall': sum(item.get('avg_price', 0) or 0 for item in data) / len(data),
            'total_promo_products': sum(item['promo_products_count'] for item in data)
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def top_expensive_products_view(request):
    try:
        limit = int(request.GET.get('limit', 10))
        
        data = list(analytics_repo.get_top_expensive_products(limit=limit))
        
        # Конвертуємо Decimal в float
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        products_with_promo = sum(1 for item in data if item.get('promo_price') is not None)
        
        statistics = {
            'avg_regular_price': sum(item['regular_price'] for item in data) / len(data),
            'avg_discount': sum(item['discount'] for item in data) / len(data),
            'products_with_promo': products_with_promo,
            'max_discount': max(item['discount'] for item in data),
            'total_potential_savings': sum(item['discount'] for item in data)
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def products_by_price_ranges_view(request):
    try:
        queryset = analytics_repo.get_products_by_price_ranges()
        
        product_type_filter = request.GET.get('product_type', None)
        if product_type_filter:
            queryset = queryset.filter(product_type_name__icontains=product_type_filter)
        
        data = list(queryset)
        
        # Конвертуємо Decimal в float
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        # Підрахунки без pandas
        range_totals = {}
        unique_ranges = set()
        unique_types = set()
        
        for item in data:
            range_name = item['price_range']
            unique_ranges.add(range_name)
            unique_types.add(item['product_type_name'])
            range_totals[range_name] = range_totals.get(range_name, 0) + item['count']
        
        most_popular_range = max(range_totals, key=range_totals.get) if range_totals else None
        
        statistics = {
            'total_products': sum(item['count'] for item in data),
            'price_ranges_count': len(unique_ranges),
            'most_popular_range': most_popular_range,
            'most_popular_range_count': range_totals.get(most_popular_range, 0) if most_popular_range else 0,
            'product_types_count': len(unique_types)
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def promo_analysis_by_store_view(request):
    try:
        queryset = analytics_repo.get_promo_analysis_by_store()
        
        city_filter = request.GET.get('city', None)
        min_promo = request.GET.get('min_promo_products', None)
        
        if city_filter:
            queryset = queryset.filter(city__icontains=city_filter)
        if min_promo:
            queryset = queryset.filter(promo_products__gte=int(min_promo))
        
        data = list(queryset)
        
        # Конвертуємо Decimal в float
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        max_promo_store = max(data, key=lambda x: x['promo_products'])
        
        statistics = {
            'total_stores': len(data),
            'total_promo_products': sum(item['promo_products'] for item in data),
            'avg_discount_percent': sum(item['avg_discount_percent'] for item in data) / len(data),
            'total_savings': sum(item['total_savings'] for item in data),
            'max_discount_percent': max(item['avg_discount_percent'] for item in data),
            'store_with_most_promos': max_promo_store['store_name']
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def product_creation_dynamics_view(request):
    try:
        queryset = analytics_repo.get_product_creation_dynamics()
        
        product_type_filter = request.GET.get('product_type', None)
        if product_type_filter:
            queryset = queryset.filter(product_type_name__icontains=product_type_filter)
        
        data = list(queryset)
        
        # Конвертуємо Decimal в float та дати в str
        for item in data:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
                elif key == 'month':
                    item[key] = str(value)
        
        if not data:
            return Response({
                'data': [],
                'statistics': {}
            })
        
        # Підрахунки без pandas
        monthly_totals = {}
        unique_months = set()
        unique_types = set()
        
        for item in data:
            month = item['month']
            unique_months.add(month)
            unique_types.add(item['product_type_name'])
            monthly_totals[month] = monthly_totals.get(month, 0) + item['products_added']
        
        peak_month = max(monthly_totals, key=monthly_totals.get) if monthly_totals else None
        
        statistics = {
            'total_months': len(unique_months),
            'total_products_added': sum(item['products_added'] for item in data),
            'avg_products_per_month': sum(monthly_totals.values()) / len(monthly_totals) if monthly_totals else 0,
            'peak_month': peak_month,
            'peak_month_count': monthly_totals.get(peak_month, 0) if peak_month else 0,
            'product_types_tracked': len(unique_types)
        }
        
        response_data = {
            'data': data,
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
