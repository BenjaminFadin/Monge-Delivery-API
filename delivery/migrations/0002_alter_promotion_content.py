# Generated by Django 3.2.12 on 2024-07-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='content',
            field=models.TextField(),
        ),
    ]
