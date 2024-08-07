# Generated by Django 3.2.12 on 2024-08-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_alter_order_payment_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='delivery_location',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='pickup_location',
            new_name='longitude',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
