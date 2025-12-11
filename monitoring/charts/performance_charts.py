from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.embed import components
from bokeh.palettes import Category10, RdYlGn11
from bokeh.transform import transform
import pandas as pd
import numpy as np


class PerformanceChartsGenerator:
    
    def create_execution_time_chart(self, df: pd.DataFrame):
        p = figure(
            title="Час виконання запитів vs Кількість воркерів",
            x_axis_label="Кількість воркерів",
            y_axis_label="Час виконання (секунди)",
            height=400,
            width=800
        )
        
        methods = df['method'].unique()
        colors = Category10[max(3, len(methods))]
        
        for method, color in zip(methods, colors):
            df_filtered = df[df['method'] == method]
            source = ColumnDataSource(df_filtered)
            
            p.line('num_workers', 'execution_time', source=source, 
                   line_width=2, color=color, legend_label=method)
            p.scatter('num_workers', 'execution_time', source=source, 
                      size=8, color=color)
        
        hover = HoverTool(tooltips=[
            ("Метод", "@method"),
            ("Воркерів", "@num_workers"),
            ("Час виконання", "@execution_time{0.3f} с"),
            ("Запитів", "@num_queries"),
            ("Успішних", "@success_count")
        ])
        p.add_tools(hover)
        
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        
        script, div = components(p)
        return script, div
    
    def create_throughput_chart(self, df: pd.DataFrame):
        p = figure(
            title="Пропускна здатність vs Кількість воркерів",
            x_axis_label="Кількість воркерів",
            y_axis_label="Пропускна здатність (запитів/сек)",
            height=400,
            width=800
        )
        
        methods = df['method'].unique()
        colors = Category10[max(3, len(methods))]
        
        for method, color in zip(methods, colors):
            df_filtered = df[df['method'] == method]
            source = ColumnDataSource(df_filtered)
            
            p.line('num_workers', 'throughput', source=source,
                   line_width=2, color=color, legend_label=method)
            p.scatter('num_workers', 'throughput', source=source,
                      size=8, color=color)
        
        hover = HoverTool(tooltips=[
            ("Метод", "@method"),
            ("Воркерів", "@num_workers"),
            ("Пропускна здатність", "@throughput{0.2f} req/s"),
            ("Час виконання", "@execution_time{0.3f} с")
        ])
        p.add_tools(hover)
        
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
        
        script, div = components(p)
        return script, div
    
    def create_heatmap_chart(self, df: pd.DataFrame):
        methods = df['method'].unique()
        workers = sorted(df['num_workers'].unique())
        
        heatmap_data = []
        for method in methods:
            for worker in workers:
                row = df[(df['method'] == method) & (df['num_workers'] == worker)]
                if not row.empty:
                    exec_time = row['execution_time'].values[0]
                    heatmap_data.append({
                        'method': method,
                        'workers': worker,
                        'execution_time': exec_time
                    })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        
        if heatmap_df.empty:
            return self._create_empty_chart("Теплова карта часу виконання")
        
        source = ColumnDataSource(heatmap_df)
        
        mapper = LinearColorMapper(
            palette=RdYlGn11[::-1],
            low=heatmap_df['execution_time'].min(),
            high=heatmap_df['execution_time'].max()
        )
        
        p = figure(
            title="Теплова карта часу виконання",
            x_axis_label="Кількість воркерів",
            y_range=list(methods),
            x_range=[str(w) for w in workers],
            toolbar_location="above",
            tools="hover,save",
            height=400,
            width=800
        )
        
        p.rect(x='workers', y='method', width=1, height=1,
               source=source,
               fill_color=transform('execution_time', mapper),
               line_color=None)
        
        hover = HoverTool(tooltips=[
            ("Метод", "@method"),
            ("Воркерів", "@workers"),
            ("Час виконання", "@execution_time{0.3f} с")
        ])
        
        script, div = components(p)
        return script, div
    
    def _create_empty_chart(self, title):
        p = figure(height=400, width=800, title=title)
        p.text(x=[0], y=[0], text=["Немає даних для відображення"])
        script, div = components(p)
        return script, div
