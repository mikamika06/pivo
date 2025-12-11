from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.repositories.analytics import AnalyticsRepository
from monitoring.charts.plotly_charts import PlotlyChartsGenerator
from monitoring.models import Store, ProductType
import pandas as pd
from datetime import datetime


analytics_repo = AnalyticsRepository()


@login_required
def dashboard_v1_view(request):
    city = request.GET.get('city', None)
    product_type_id = request.GET.get('product_type', None)
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    price_min = float(request.GET.get('price_min', 0))
    price_max = float(request.GET.get('price_max', 10000))
    
    data1 = analytics_repo.get_avg_prices_by_product_type()
    data2 = analytics_repo.get_store_statistics_by_city()
    data3 = analytics_repo.get_top_expensive_products(limit=10)
    data4 = analytics_repo.get_products_by_price_ranges()
    data5 = analytics_repo.get_promo_analysis_by_store()
    data6 = analytics_repo.get_product_creation_dynamics()
    
    df1 = pd.DataFrame(list(data1))
    df2 = pd.DataFrame(list(data2))
    df3 = pd.DataFrame(list(data3))
    df4 = pd.DataFrame(list(data4))
    df5 = pd.DataFrame(list(data5))
    df6 = pd.DataFrame(list(data6))
    
    if city:
        if not df2.empty:
            df2 = df2[df2['city'] == city]
        if not df3.empty:
            df3 = df3[df3['city'] == city]
        if not df5.empty:
            df5 = df5[df5['city'] == city]
    
    if product_type_id:
        try:
            product_type_id = int(product_type_id)
            if not df1.empty:
                df1 = df1[df1.get('product_type_id', pd.Series()) == product_type_id]
            if not df4.empty:
                df4 = df4[df4.get('product_type_id', pd.Series()) == product_type_id]
        except (ValueError, TypeError):
            pass
    
    if not df3.empty and 'regular_price' in df3.columns:
        df3 = df3[(df3['regular_price'] >= price_min) & (df3['regular_price'] <= price_max)]
    
    if date_from and not df6.empty and 'month' in df6.columns:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
            df6 = df6[pd.to_datetime(df6['month']).dt.date >= date_from_parsed]
        except (ValueError, TypeError):
            pass
    
    if date_to and not df6.empty and 'month' in df6.columns:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
            df6 = df6[pd.to_datetime(df6['month']).dt.date <= date_to_parsed]
        except (ValueError, TypeError):
            pass
    
    chart_generator = PlotlyChartsGenerator()
    
    chart1 = chart_generator.create_avg_prices_chart(df1)
    chart2 = chart_generator.create_store_statistics_chart(df2)
    chart3 = chart_generator.create_top_expensive_products_chart(df3)
    chart4 = chart_generator.create_price_ranges_chart(df4)
    chart5 = chart_generator.create_promo_analysis_chart(df5)
    chart6 = chart_generator.create_product_dynamics_chart(df6)
    
    cities = Store.objects.values_list('city', flat=True).distinct().order_by('city')
    product_types = ProductType.objects.all().order_by('name')
    
    stats = {
        'total_stores': Store.objects.filter(is_active=True).count(),
        'total_product_types': ProductType.objects.filter(is_active=True).count(),
        'total_products': df1['product_count'].sum() if not df1.empty and 'product_count' in df1.columns else 0,
    }
    
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
        'cities': cities,
        'product_types': product_types,
        'selected_city': city,
        'selected_product_type': product_type_id,
        'date_from': date_from,
        'date_to': date_to,
        'price_min': price_min,
        'price_max': price_max,
        'stats': stats,
    }
    
    return render(request, 'monitoring/dashboard_v1.html', context)
