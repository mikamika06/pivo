
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoring", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active'], name='product_is_active_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product_type_id'], name='product_type_id_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['store_id'], name='product_store_id_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['regular_price'], name='product_regular_price_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['promo_price'], name='product_promo_price_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_at'], name='product_created_at_idx'),
        ),
        
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'product_type_id'], name='product_active_type_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'store_id'], name='product_active_store_idx'),
        ),
        
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['city'], name='store_city_idx'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['is_active'], name='store_is_active_idx'),
        ),
    ]
