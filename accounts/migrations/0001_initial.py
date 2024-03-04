# Generated by Django 5.0.2 on 2024-03-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50, verbose_name='اسم')),
                ('last_name', models.CharField(max_length=50, verbose_name='نام خوانوادگی')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ادرس ایمیل')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='شماره تماس')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت نام')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='اخرین ورود')),
                ('is_admin', models.BooleanField(default=False, verbose_name='کاربر مورد نظر ادمین است ؟')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کاربر مورد نظر کارمند است ؟')),
                ('is_active', models.BooleanField(default=False, verbose_name='کاربر مورد نظر فعال است ؟')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='کاربر مورد نظر ادمین اصلی است ؟')),
            ],
            options={
                'verbose_name': 'اکانت',
                'verbose_name_plural': 'اکانت\u200cها',
            },
        ),
    ]
