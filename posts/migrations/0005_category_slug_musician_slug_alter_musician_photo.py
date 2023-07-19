# Generated by Django 4.1.7 on 2023-04-07 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_category_options_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='dsad', max_length=255, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='musician',
            name='slug',
            field=models.SlugField(default='dsadasd', max_length=255, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
