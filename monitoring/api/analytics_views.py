
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

from monitoring.repositories.analytics import AnalyticsRepository


analytics_repo = AnalyticsRepository()


@api_view(['GET'])
@permission_classes([AllowAny])  
def avg_prices_by_product_type_view(request):
    try:
        data = analytics_repo.get_avg_prices_by_product_type()
        
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        statistics = {
            'total_product_types': len(df),
            'avg_regular_price_overall': float(df['avg_regular_price'].mean()),
            'avg_promo_price_overall': float(df['avg_promo_price'].mean()),
            'total_products': int(df['product_count'].sum()),
            'max_avg_regular_price': float(df['avg_regular_price'].max()),
            'min_avg_regular_price': float(df['avg_regular_price'].min())
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
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
        data = analytics_repo.get_store_statistics_by_city()
        
        city_filter = request.GET.get('city', None)
        if city_filter:
            data = data.filter(city__icontains=city_filter)
        
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        statistics = {
            'total_cities': len(df),
            'total_stores': int(df['store_count'].sum()),
            'total_products': int(df['total_products'].sum()),
            'avg_products_per_store': float(df['total_products'].sum() / df['store_count'].sum()),
            'avg_price_overall': float(df['avg_price'].mean()),
            'total_promo_products': int(df['promo_products_count'].sum())
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
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
        
        data = analytics_repo.get_top_expensive_products(limit=limit)
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        statistics = {
            'avg_regular_price': float(df['regular_price'].mean()),
            'avg_discount': float(df['discount'].mean()),
            'products_with_promo': int(df['promo_price'].notna().sum()),
            'max_discount': float(df['discount'].max()),
            'total_potential_savings': float(df['discount'].sum())
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
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
        data = analytics_repo.get_products_by_price_ranges()
        
        product_type_filter = request.GET.get('product_type', None)
        if product_type_filter:
            data = data.filter(product_type_name__icontains=product_type_filter)
        
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        range_totals = df.groupby('price_range')['count'].sum()
        most_popular_range = range_totals.idxmax()
        
        statistics = {
            'total_products': int(df['count'].sum()),
            'price_ranges_count': len(df['price_range'].unique()),
            'most_popular_range': most_popular_range,
            'most_popular_range_count': int(range_totals.max()),
            'product_types_count': len(df['product_type_name'].unique())
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
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
        data = analytics_repo.get_promo_analysis_by_store()
        
        city_filter = request.GET.get('city', None)
        min_promo = request.GET.get('min_promo_products', None)
        
        if city_filter:
            data = data.filter(city__icontains=city_filter)
        if min_promo:
            data = data.filter(promo_products__gte=int(min_promo))
        
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        statistics = {
            'total_stores': len(df),
            'total_promo_products': int(df['promo_products'].sum()),
            'avg_discount_percent': float(df['avg_discount_percent'].mean()),
            'total_savings': float(df['total_savings'].sum()),
            'max_discount_percent': float(df['avg_discount_percent'].max()),
            'store_with_most_promos': df.loc[df['promo_products'].idxmax(), 'store_name']
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
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
        data = analytics_repo.get_product_creation_dynamics()
        
        product_type_filter = request.GET.get('product_type', None)
        if product_type_filter:
            data = data.filter(product_type_name__icontains=product_type_filter)
        
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return Response({
                'data': [],
                'shape': [0, 0],
                'columns': [],
                'statistics': {}
            })
        
        df['month'] = df['month'].astype(str)
        
        monthly_totals = df.groupby('month')['products_added'].sum()
        peak_month = monthly_totals.idxmax()
        
        statistics = {
            'total_months': len(df['month'].unique()),
            'total_products_added': int(df['products_added'].sum()),
            'avg_products_per_month': float(df.groupby('month')['products_added'].sum().mean()),
            'peak_month': peak_month,
            'peak_month_count': int(monthly_totals.max()),
            'product_types_tracked': len(df['product_type_name'].unique())
        }
        
        response_data = {
            'data': df.to_dict(orient='records'),
            'shape': list(df.shape),
            'columns': list(df.columns),
            'statistics': statistics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
