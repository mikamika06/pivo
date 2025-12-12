from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.repositories.analytics import AnalyticsRepository
from monitoring.charts.bokeh_charts import BokehChartsGenerator
from bokeh.resources import CDN
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


def _convert_decimals_in_list(data):
    """Конвертує Decimal в float у списку словників"""
    result = []
    for item in data:
        converted_item = {}
        for key, value in item.items():
            if isinstance(value, Decimal):
                converted_item[key] = float(value)
            else:
                converted_item[key] = value
        result.append(converted_item)
    return result


@login_required
def dashboard_v2_view(request):
    try:
        analytics_repo = AnalyticsRepository()
        charts_generator = BokehChartsGenerator()
        
        # Конвертуємо QuerySet в list та Decimal в float
        avg_prices_data = _convert_decimals_in_list(list(analytics_repo.get_avg_prices_by_product_type()))
        avg_prices_script, avg_prices_div = charts_generator.create_avg_prices_chart_bokeh(avg_prices_data)
        
        store_stats_data = _convert_decimals_in_list(list(analytics_repo.get_store_statistics_by_city()))
        store_stats_script, store_stats_div = charts_generator.create_store_statistics_chart(store_stats_data)
        
        top_products_data = _convert_decimals_in_list(list(analytics_repo.get_top_expensive_products()))
        top_products_script, top_products_div = charts_generator.create_top_expensive_products_chart(top_products_data)
        
        price_ranges_data = _convert_decimals_in_list(list(analytics_repo.get_products_by_price_ranges()))
        price_ranges_script, price_ranges_div = charts_generator.create_price_ranges_chart(price_ranges_data)
        
        promo_data = _convert_decimals_in_list(list(analytics_repo.get_promo_analysis_by_store()))
        promo_script, promo_div = charts_generator.create_promo_analysis_chart(promo_data)
        
        dynamics_data = _convert_decimals_in_list(list(analytics_repo.get_product_creation_dynamics()))
        dynamics_script, dynamics_div = charts_generator.create_product_creation_dynamics_chart(dynamics_data)
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
    
    context = {
        'bokeh_css': CDN.css_files[0] if CDN.css_files else '',
        'bokeh_js': CDN.js_files[0] if CDN.js_files else '',
        'avg_prices_script': avg_prices_script,
        'avg_prices_div': avg_prices_div,
        'store_stats_script': store_stats_script,
        'store_stats_div': store_stats_div,
        'top_products_script': top_products_script,
        'top_products_div': top_products_div,
        'price_ranges_script': price_ranges_script,
        'price_ranges_div': price_ranges_div,
        'promo_script': promo_script,
        'promo_div': promo_div,
        'dynamics_script': dynamics_script,
        'dynamics_div': dynamics_div,
    }
    
    return render(request, 'monitoring/dashboard_v2.html', context)
