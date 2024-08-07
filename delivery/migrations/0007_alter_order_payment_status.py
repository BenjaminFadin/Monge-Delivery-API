# Generated by Django 3.2.12 on 2024-08-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('В ожидании', 'В ожидании'), ('На доставке', 'На доставке'), ('Успешно доставлен', 'Успешно доставлен'), ('Отменено', 'Отменено')], default='В ожидании', max_length=100),
        ),
    ]
