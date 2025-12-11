import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class PlotlyChartsGenerator:
    
    def create_avg_prices_chart(self, df):
        if df.empty:
            return self._create_empty_chart("Середні ціни за типами продукту")
        
        fig = go.Figure(data=[
            go.Bar(name='Регулярна ціна', x=df['product_type_name'], y=df['avg_regular_price']),
            go.Bar(name='Промо ціна', x=df['product_type_name'], y=df['avg_promo_price'])
        ])
        
        fig.update_layout(
            title='Середні ціни за типами продукту',
            xaxis_title='Тип продукту',
            yaxis_title='Ціна (грн)',
            barmode='group',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_store_statistics_chart(self, df):
        if df.empty:
            return self._create_empty_chart("Статистика магазинів за містами")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['city'],
            y=df['total_products'],
            mode='lines+markers',
            name='Всього товарів'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['city'],
            y=df['promo_products_count'],
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
    
    def create_top_expensive_products_chart(self, df):
        if df.empty:
            return self._create_empty_chart("Топ-10 найдорожчих продуктів")
        
        if 'regular_price' in df.columns:
            df['regular_price'] = pd.to_numeric(df['regular_price'], errors='coerce')
        if 'promo_price' in df.columns:
            df['promo_price'] = pd.to_numeric(df['promo_price'], errors='coerce')
        
        df_sorted = df.nlargest(10, 'regular_price')
        df_sorted['short_name'] = df_sorted['product_name'].str[:35] + '...'
        
        type_colors = {
            'Beer': '#FFA500', 'Wine': '#8B0000', 'Whiskey': '#D4AF37',
            'Vodka': '#87CEEB', 'Cognac': '#654321', 'Champagne': '#FFD700',
            'Liqueur': '#FF69B4', 'Rum': '#8B4513'
        }
        df_sorted['color'] = df_sorted['product_type_name'].map(lambda x: type_colors.get(x, '#808080'))
        
        fig = go.Figure(go.Bar(
            x=df_sorted['regular_price'],
            y=df_sorted['short_name'],
            orientation='h',
            marker=dict(color=df_sorted['color']),
            text=df_sorted['regular_price'].round(2),
            textposition='outside',
            hovertemplate='<b>%{customdata[0]}</b><br>Ціна: %{x:.2f} грн<br>Тип: %{customdata[1]}<extra></extra>',
            customdata=df_sorted[['product_name', 'product_type_name']]
        ))
        
        fig.update_layout(
            title='Топ-10 найдорожчих продуктів',
            xaxis_title='Ціна (грн)',
            yaxis_title='',
            height=500,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_price_ranges_chart(self, df):
        if df.empty:
            return self._create_empty_chart("Розподіл товарів за ціновими діапазонами")
        
        type_colors = {
            'Beer': '#FFA500', 'Champagne': '#FFD700', 'Cognac': '#654321',
            'Liqueur': '#FF69B4', 'Rum': '#8B4513', 'Vodka': '#87CEEB',
            'Whiskey': '#D4AF37', 'Wine': '#8B0000'
        }
        
        fig = px.bar(
            df,
            x='price_range',
            y='count',
            color='product_type_name',
            title='Розподіл товарів за ціновими діапазонами',
            labels={'price_range': 'Ціновий діапазон', 'count': 'Кількість', 'product_type_name': 'Тип'},
            color_discrete_map=type_colors
        )
        
        fig.update_layout(height=450, barmode='stack')
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_promo_analysis_chart(self, df):
        if df.empty:
            return self._create_empty_chart("Аналіз промо-акцій")
        
        if 'total_savings' in df.columns:
            df['total_savings'] = pd.to_numeric(df['total_savings'], errors='coerce')
        if 'avg_discount_percent' in df.columns:
            df['avg_discount_percent'] = pd.to_numeric(df['avg_discount_percent'], errors='coerce')
        
        df_top = df.nlargest(15, 'total_savings').sort_values('total_savings')
        
        fig = go.Figure(go.Bar(
            x=df_top['total_savings'],
            y=df_top['store_name'],
            orientation='h',
            marker=dict(color='#2ca02c'),
            text=df_top['total_savings'].round(0),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Економія: %{x:,.0f} грн<br>Місто: %{customdata[0]}<br>Промо товарів: %{customdata[1]}<br>Знижка: %{customdata[2]:.1f}%<extra></extra>',
            customdata=df_top[['city', 'promo_products', 'avg_discount_percent']]
        ))
        
        fig.update_layout(
            title='Топ-15 магазинів за економією на промо-акціях',
            xaxis_title='Загальна економія (грн)',
            yaxis_title='',
            height=600,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_product_dynamics_chart(self, df):
        from monitoring.models import Product, ProductType
        from django.db.models import Count, Q
        
        promo_data = ProductType.objects.filter(
            products__is_active=True
        ).annotate(
            total_products=Count('products'),
            promo_products=Count('products', filter=Q(products__promo_price__isnull=False)),
            regular_products=Count('products', filter=Q(products__promo_price__isnull=True))
        ).values('name', 'total_products', 'promo_products', 'regular_products').order_by('-total_products')
        
        df_promo = pd.DataFrame(list(promo_data))
        
        if df_promo.empty:
            return self._create_empty_chart("Промо vs Регулярні")
        
        df_promo['promo_percent'] = (df_promo['promo_products'] / df_promo['total_products'] * 100).round(1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Промо товари',
            x=df_promo['name'],
            y=df_promo['promo_products'],
            marker_color='#2ca02c',
            text=df_promo['promo_products'],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Регулярні товари',
            x=df_promo['name'],
            y=df_promo['regular_products'],
            marker_color='#1f77b4',
            text=df_promo['regular_products'],
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
