# Generated by Django 3.2.12 on 2024-08-04 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='delivery.order'),
            preserve_default=False,
        ),
    ]
