import plotly.graph_objects as go
import plotly.express as px


class PlotlyChartsGenerator:
    
    def create_avg_prices_chart(self, data):
        # data - вже list of dict з API
        if not data:
            return self._create_empty_chart("Середні ціни за типами продукту")
        
        product_types = [item['product_type_name'] for item in data]
        avg_regular = [item['avg_regular_price'] for item in data]
        avg_promo = [item.get('avg_promo_price', 0) or 0 for item in data]
        
        fig = go.Figure(data=[
            go.Bar(name='Регулярна ціна', x=product_types, y=avg_regular),
            go.Bar(name='Промо ціна', x=product_types, y=avg_promo)
        ])
        
        fig.update_layout(
            title='Середні ціни за типами продукту',
            xaxis_title='Тип продукту',
            yaxis_title='Ціна (грн)',
            barmode='group',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_store_statistics_chart(self, data):
        # data - вже list of dict з API
        if not data:
            return self._create_empty_chart("Статистика магазинів за містами")
        
        cities = [item['city'] for item in data]
        total_products = [item['total_products'] for item in data]
        promo_products = [item['promo_products_count'] for item in data]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=cities,
            y=total_products,
            mode='lines+markers',
            name='Всього товарів'
        ))
        
        fig.add_trace(go.Scatter(
            x=cities,
            y=promo_products,
            mode='lines+markers',
            name='Промо товарів'
        ))
        
        fig.update_layout(
            title='Статистика магазинів за містами',
            xaxis_title='Місто',
            yaxis_title='Кількість',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_top_expensive_products_chart(self, data):
        # data - вже list of dict з API
        if not data:
            return self._create_empty_chart("Топ-10 найдорожчих продуктів")
        
        # Сортуємо та беремо топ-10
        sorted_data = sorted(data, key=lambda x: float(x.get('regular_price', 0) or 0), reverse=True)[:10]
        
        for item in sorted_data:
            item['short_name'] = item['product_name'][:35] + '...'
        
        type_colors = {
            'Beer': '#FFA500', 'Wine': '#8B0000', 'Whiskey': '#D4AF37',
            'Vodka': '#87CEEB', 'Cognac': '#654321', 'Champagne': '#FFD700',
            'Liqueur': '#FF69B4', 'Rum': '#8B4513'
        }
        colors = [type_colors.get(item['product_type_name'], '#808080') for item in sorted_data]
        
        short_names = [item['short_name'] for item in sorted_data]
        prices = [float(item['regular_price']) for item in sorted_data]
        product_names = [item['product_name'] for item in sorted_data]
        product_types = [item['product_type_name'] for item in sorted_data]
        
        fig = go.Figure(go.Bar(
            x=prices,
            y=short_names,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{p:.2f}" for p in prices],
            textposition='outside',
            hovertemplate='<b>%{customdata[0]}</b><br>Ціна: %{x:.2f} грн<br>Тип: %{customdata[1]}<extra></extra>',
            customdata=list(zip(product_names, product_types))
        ))
        
        fig.update_layout(
            title='Топ-10 найдорожчих продуктів',
            xaxis_title='Ціна (грн)',
            yaxis_title='',
            height=500,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_price_ranges_chart(self, data):
        # data - вже list of dict з API
        if not data:
            return self._create_empty_chart("Розподіл товарів за ціновими діапазонами")
        
        type_colors = {
            'Beer': '#FFA500', 'Champagne': '#FFD700', 'Cognac': '#654321',
            'Liqueur': '#FF69B4', 'Rum': '#8B4513', 'Vodka': '#87CEEB',
            'Whiskey': '#D4AF37', 'Wine': '#8B0000'
        }
        
        # Перетворюємо в формат для plotly
        price_ranges = [item['price_range'] for item in data]
        counts = [item['count'] for item in data]
        types = [item['product_type_name'] for item in data]
        
        fig = px.bar(
            x=price_ranges,
            y=counts,
            color=types,
            title='Розподіл товарів за ціновими діапазонами',
            labels={'x': 'Ціновий діапазон', 'y': 'Кількість', 'color': 'Тип'},
            color_discrete_map=type_colors
        )
        
        fig.update_layout(height=450, barmode='stack')
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_promo_analysis_chart(self, data):
        # data - вже list of dict з API
        if not data:
            return self._create_empty_chart("Аналіз промо-акцій")
        
        # Сортуємо та беремо топ-15
        sorted_data = sorted(data, key=lambda x: float(x.get('total_savings', 0) or 0), reverse=True)[:15]
        sorted_data = sorted(sorted_data, key=lambda x: float(x.get('total_savings', 0) or 0))
        
        store_names = [item['store_name'] for item in sorted_data]
        total_savings = [float(item['total_savings']) for item in sorted_data]
        cities = [item['city'] for item in sorted_data]
        promo_products = [item['promo_products'] for item in sorted_data]
        avg_discounts = [float(item['avg_discount_percent']) for item in sorted_data]
        
        fig = go.Figure(go.Bar(
            x=total_savings,
            y=store_names,
            orientation='h',
            marker=dict(color='#2ca02c'),
            text=[f"{s:.0f}" for s in total_savings],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Економія: %{x:,.0f} грн<br>Місто: %{customdata[0]}<br>Промо товарів: %{customdata[1]}<br>Знижка: %{customdata[2]:.1f}%<extra></extra>',
            customdata=list(zip(cities, promo_products, avg_discounts))
        ))
        
        fig.update_layout(
            title='Топ-15 магазинів за економією на промо-акціях',
            xaxis_title='Загальна економія (грн)',
            yaxis_title='',
            height=600,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_product_dynamics_chart(self, data):
        from monitoring.models import Product, ProductType
        from django.db.models import Count, Q
        
        promo_data = ProductType.objects.filter(
            products__is_active=True
        ).annotate(
            total_products=Count('products'),
            promo_products=Count('products', filter=Q(products__promo_price__isnull=False)),
            regular_products=Count('products', filter=Q(products__promo_price__isnull=True))
        ).values('name', 'total_products', 'promo_products', 'regular_products').order_by('-total_products')
        
        promo_list = list(promo_data)
        
        if not promo_list:
            return self._create_empty_chart("Промо vs Регулярні")
        
        for item in promo_list:
            item['promo_percent'] = round((item['promo_products'] / item['total_products'] * 100), 1) if item['total_products'] > 0 else 0
        
        names = [item['name'] for item in promo_list]
        promo_prods = [item['promo_products'] for item in promo_list]
        regular_prods = [item['regular_products'] for item in promo_list]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Промо товари',
            x=names,
            y=promo_prods,
            marker_color='#2ca02c',
            text=promo_prods,
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Регулярні товари',
            x=names,
            y=regular_prods,
            marker_color='#1f77b4',
            text=regular_prods,
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Порівняння промо та регулярних товарів за типами',
            xaxis_title='Тип продукту',
            yaxis_title='Кількість товарів',
            barmode='group',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_empty_chart(self, title):
        fig = go.Figure()
        fig.add_annotation(
            text="Немає даних для відображення",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        fig.update_layout(title=title, height=400)
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
