# Generated by Django 5.0.2 on 2024-03-06 05:13

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypesFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(choices=[('صفحه نمایش', 'صفحه نمایش'), ('دوربین', 'دوربین'), ('باتری', 'باتری'), ('شارژ', 'شارژر'), ('رنگ', 'رنگ')], max_length=80, verbose_name='ویژگی خاص محصول')),
                ('feature_value', models.CharField(max_length=250, verbose_name='توضیح ویژگی محصول')),
                ('stock', models.IntegerField(default=1, verbose_name='موجودی محصول')),
                ('is_active', models.BooleanField(default=True, verbose_name='نمایش عمومی')),
            ],
            options={
                'verbose_name': 'ویژگی منحصربفرد محصول',
                'verbose_name_plural': 'ویژگی های منحصر بفرد محصول',
            },
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='title', unique=True, verbose_name='ادرس'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='title', unique=True, verbose_name='ادرس'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/', verbose_name='کاور'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_brand', to='BaseApp.brand', verbose_name='برند'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='BaseApp.category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='تخفیف محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='title', unique=True, verbose_name='ادرس'),
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(related_name='product_features', to='BaseApp.typesfeature', verbose_name='جزییات'),
        ),
        migrations.DeleteModel(
            name='types_features',
        ),
    ]
