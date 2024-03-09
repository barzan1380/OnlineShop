# Generated by Django 5.0.2 on 2024-03-06 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0002_typesfeature_alter_brand_slug_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AlterField(
            model_name='typesfeature',
            name='feature_key',
            field=models.CharField(choices=[('scren page', 'صفحه نمایش'), ('cammera', 'دوربین'), ('battrey', 'باتری'), ('adaptor', 'شارژر'), ('color', 'رنگ')], max_length=80, verbose_name='ویژگی خاص محصول'),
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(verbose_name='موجودی محصول')),
                ('price', models.IntegerField(verbose_name='قیمت محصول')),
                ('discount', models.IntegerField(default=0, verbose_name='تخفیف محصول')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='زمان بارگزاری')),
                ('available', models.BooleanField(verbose_name='در دسترسه؟')),
                ('features', models.ManyToManyField(to='BaseApp.typesfeature', verbose_name='ویژگی های متغیر محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BaseApp.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'متغیر محصول',
                'verbose_name_plural': 'متغیر های محصول',
            },
        ),
    ]