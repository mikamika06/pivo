from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from monitoring.repositories.analytics import AnalyticsRepository
from monitoring.charts.plotly_charts import PlotlyChartsGenerator
from monitoring.models import Store, ProductType, Product
import pandas as pd
from datetime import datetime


analytics_repo = AnalyticsRepository()


@login_required
def dashboard_v1_view(request):
    # Пагінація продуктів
    page_number = request.GET.get('page', 1)
    products_list = Product.objects.select_related('product_type', 'store').order_by('-created_at')
    paginator = Paginator(products_list, 20)  # 20 продуктів на сторінку
    page_obj = paginator.get_page(page_number)
    
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
    
    chart_generator = PlotlyChartsGenerator()
    
    chart1 = chart_generator.create_avg_prices_chart(df1)
    chart2 = chart_generator.create_store_statistics_chart(df2)
    chart3 = chart_generator.create_top_expensive_products_chart(df3)
    chart4 = chart_generator.create_price_ranges_chart(df4)
    chart5 = chart_generator.create_promo_analysis_chart(df5)
    chart6 = chart_generator.create_product_dynamics_chart(df6)
    
    stats = {
        'total_stores': Store.objects.filter(is_active=True).count(),
        'total_product_types': ProductType.objects.filter(is_active=True).count(),
        'total_products': Product.objects.count(),
    }
    
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
        'stats': stats,
        'page_obj': page_obj,
    }
    
    return render(request, 'monitoring/dashboard_v1.html', context)
