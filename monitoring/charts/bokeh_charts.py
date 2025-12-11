from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import dodge
from bokeh.palettes import Category20_3, Category10
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd
from collections import defaultdict
from decimal import Decimal


class BokehChartsGenerator:
    
    def _convert_decimals(self, df):
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    if any(isinstance(x, Decimal) for x in df[col].dropna()[:5]):
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
                except:
                    pass
        return df
    
    def create_avg_prices_chart_bokeh(self, data):
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return self._create_empty_chart("Середні ціни за типами продукту")
        
        df = self._convert_decimals(df)
        
        source = ColumnDataSource(df)
        product_types = df['product_type_name'].tolist()
        
        p = figure(
            x_range=product_types,
            height=400,
            title="Середні ціни за типами продукту",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        p.vbar(
            x=dodge('product_type_name', -0.15, range=p.x_range),
            top='avg_regular_price',
            width=0.25,
            source=source,
            color='#c9d9d3',
            legend_label="Регулярна ціна"
        )
        
        p.vbar(
            x=dodge('product_type_name', 0.15, range=p.x_range),
            top='avg_promo_price',
            width=0.25,
            source=source,
            color='#718dbf',
            legend_label="Промо ціна"
        )
        
        hover = HoverTool(tooltips=[
            ("Тип", "@product_type_name"),
            ("Регулярна ціна", "@avg_regular_price{0.2f} грн"),
            ("Промо ціна", "@avg_promo_price{0.2f} грн"),
            ("Кількість товарів", "@product_count")
        ])
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Тип продукту"
        p.yaxis.axis_label = "Ціна (грн)"
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        
        script, div = components(p)
        return script, div
    
    def create_store_statistics_chart(self, data):
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return self._create_empty_chart("Статистика магазинів за містами")
        
        df = self._convert_decimals(df)
        
        cities = df['city'].tolist()
        
        p = figure(
            x_range=cities,
            height=400,
            title="Статистика магазинів за містами",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        source = ColumnDataSource(df)
        
        p.line(x='city', y='total_products', source=source, 
               line_width=2, color='#1f77b4', legend_label='Всього товарів')
        p.scatter(x='city', y='total_products', source=source, 
                  size=8, color='#1f77b4')
        
        p.line(x='city', y='promo_products_count', source=source,
               line_width=2, color='#ff7f0e', legend_label='Промо товарів')
        p.scatter(x='city', y='promo_products_count', source=source,
                  size=8, color='#ff7f0e')
        
        hover = HoverTool(tooltips=[
            ("Місто", "@city"),
            ("Магазинів", "@store_count"),
            ("Всього товарів", "@total_products"),
            ("Промо товарів", "@promo_products_count"),
            ("Середня ціна", "@avg_price{0.2f} грн")
        ])
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Місто"
        p.yaxis.axis_label = "Кількість"
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        p.xaxis.major_label_orientation = 0.8
        
        script, div = components(p)
        return script, div
    
    def create_top_expensive_products_chart(self, data):
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return self._create_empty_chart("Топ-10 найдорожчих продуктів")
        
        df = self._convert_decimals(df)
        df = df.nlargest(10, 'regular_price')
        
        df['short_name'] = df['product_name'].str[:30] + '...'
        
        type_colors = {
            'Beer': '#FFA500',
            'Wine': '#8B0000',
            'Whiskey': '#D4AF37',
            'Vodka': '#87CEEB',
            'Cognac': '#654321',
            'Champagne': '#FFD700',
            'Liqueur': '#FF69B4',
            'Rum': '#8B4513'
        }
        df['color'] = df['product_type_name'].map(lambda x: type_colors.get(x, '#808080'))
        
        source = ColumnDataSource(df)
        product_names = df['short_name'].tolist()
        
        p = figure(
            y_range=product_names,
            height=500,
            width=800,
            title="Топ-10 найдорожчих продуктів",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        p.hbar(y='short_name', right='regular_price', source=source,
               height=0.7, color='color', alpha=0.8)
        
        hover = HoverTool(tooltips=[
            ("Продукт", "@product_name"),
            ("Тип", "@product_type_name"),
            ("Ціна", "@regular_price{0.2f} грн"),
            ("Місто", "@city"),
            ("Магазин", "@store_name")
        ])
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Ціна (грн)"
        p.yaxis.axis_label = ""
        p.xgrid.grid_line_color = None
        
        script, div = components(p)
        return script, div
    
    def create_price_ranges_chart(self, data):
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return self._create_empty_chart("Розподіл товарів за ціновими діапазонами")
        
        df = self._convert_decimals(df)
        
        price_ranges = ['0-30 грн', '30-60 грн', '60-100 грн', '100+ грн']
        
        product_types = sorted(df['product_type_name'].unique())
        
        range_data = defaultdict(lambda: defaultdict(int))
        for _, row in df.iterrows():
            range_data[row['price_range']][row['product_type_name']] = int(row['count'])
        
        data_dict = {'price_range': price_ranges}
        for pt in product_types:
            data_dict[pt] = [int(range_data[pr].get(pt, 0)) for pr in price_ranges]
        
        type_colors = {
            'Beer': '#FFA500',
            'Champagne': '#FFD700',
            'Cognac': '#654321',
            'Liqueur': '#FF69B4',
            'Rum': '#8B4513',
            'Vodka': '#87CEEB',
            'Whiskey': '#D4AF37',
            'Wine': '#8B0000'
        }
        colors = [type_colors.get(pt, '#808080') for pt in product_types]
        
        p = figure(
            x_range=price_ranges,
            height=450,
            width=900,
            title="Розподіл товарів за ціновими діапазонами",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        source = ColumnDataSource(data=data_dict)
        
        renderers = p.vbar_stack(
            product_types, x='price_range', width=0.7,
            color=colors, source=source,
            legend_label=list(product_types), alpha=0.8
        )
        
        p.xaxis.axis_label = "Ціновий діапазон"
        p.yaxis.axis_label = "Кількість товарів"
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        p.legend.label_text_font_size = "10pt"
        p.xaxis.major_label_text_font_size = "11pt"
        
        script, div = components(p)
        return script, div
    
    def create_promo_analysis_chart(self, data):
        df = pd.DataFrame(list(data))
        
        if df.empty:
            return self._create_empty_chart("Аналіз промо-акцій")
        
        df = self._convert_decimals(df)
        df = df.nlargest(15, 'total_savings')
        df = df.sort_values('avg_discount_percent')
        
        source = ColumnDataSource(df)
        stores = df['store_name'].tolist()
        
        p = figure(
            y_range=stores,
            height=600,
            width=900,
            title="Топ-15 магазинів за економією на промо-акціях",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        p.hbar(y='store_name', right='total_savings', source=source,
               height=0.6, color='#2ca02c', alpha=0.8)
        
        hover = HoverTool(tooltips=[
            ("Магазин", "@store_name"),
            ("Місто", "@city"),
            ("Промо товарів", "@promo_products"),
            ("Середня знижка", "@avg_discount_percent{0.1f}%"),
            ("Загальна економія", "@total_savings{0,0} грн")
        ])
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Загальна економія (грн)"
        p.yaxis.axis_label = ""
        p.xaxis.axis_label_text_font_size = "12pt"
        p.xgrid.grid_line_color = None
        
        script, div = components(p)
        return script, div
    
    def create_product_creation_dynamics_chart(self, data):
        from monitoring.models import Product, ProductType
        from django.db.models import Count, Q
        
        promo_data = ProductType.objects.filter(
            products__is_active=True
        ).annotate(
            total_products=Count('products'),
            promo_products=Count('products', filter=Q(products__promo_price__isnull=False)),
            regular_products=Count('products', filter=Q(products__promo_price__isnull=True))
        ).values('name', 'total_products', 'promo_products', 'regular_products').order_by('-total_products')
        
        df = pd.DataFrame(list(promo_data))
        
        if df.empty:
            return self._create_empty_chart("Промо vs Регулярні товари")
        
        df = self._convert_decimals(df)
        df['promo_percent'] = (df['promo_products'] / df['total_products'] * 100).round(1)
        
        product_types = df['name'].tolist()
        
        p = figure(
            x_range=product_types,
            height=500,
            width=900,
            title="Порівняння промо та регулярних товарів за типами",
            toolbar_location="above",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        source = ColumnDataSource(df)
        
        p.vbar(x='name', top='promo_products', source=source,
               width=0.35, color='#2ca02c', legend_label='Промо товари', alpha=0.8)
        
        p.vbar(x=dodge('name', 0.35, range=p.x_range), top='regular_products', source=source,
               width=0.35, color='#1f77b4', legend_label='Регулярні товари', alpha=0.8)
        
        hover = HoverTool(tooltips=[
            ("Тип", "@name"),
            ("Всього", "@total_products"),
            ("Промо", "@promo_products"),
            ("Регулярні", "@regular_products"),
            ("Промо %", "@promo_percent%")
        ])
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Тип продукту"
        p.yaxis.axis_label = "Кількість товарів"
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        p.xaxis.major_label_orientation = 0.8
        
        script, div = components(p)
        return script, div
    
    def _create_empty_chart(self, title):
        p = figure(height=400, title=title)
        p.text(x=[0], y=[0], text=["Немає даних для відображення"])
        script, div = components(p)
        return script, div
