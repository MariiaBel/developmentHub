# Generated by Django 2.2 on 2021-01-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210119_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Укажите адрес для группы. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Слаг'),
        ),
    ]