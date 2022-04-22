# Generated by Django 4.0.3 on 2022-04-18 07:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('featured', models.BooleanField(default=0)),
                ('addition_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updation_date', models.DateTimeField(auto_now=True, null=True)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='categoryimages')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcatname', models.CharField(max_length=100)),
                ('subcatdescription', models.TextField(max_length=500)),
                ('subcategory_image', models.ImageField(blank=True, null=True, upload_to='subcatimages')),
                ('catid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=100)),
                ('productdescription', ckeditor.fields.RichTextField(max_length=5000)),
                ('price', models.IntegerField()),
                ('product_image1', models.ImageField(blank=True, null=True, upload_to='productimages')),
                ('product_image2', models.ImageField(blank=True, null=True, upload_to='productimages')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to='productimages')),
                ('discount', models.IntegerField(null=True)),
                ('catid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.category')),
                ('subcatid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('zipcode', models.IntegerField()),
                ('address', models.CharField(max_length=500)),
                ('payment_mode', models.CharField(choices=[('wallet', 'Paytm/GooglePay'), ('bank', 'Bank Deposit')], max_length=15)),
                ('order_status', models.CharField(choices=[('Order Pending', 'Order is pending'), ('In Process', 'Order in Process'), ('Order Shipped', 'Order Shipped'), ('Order completed', 'Order Completed')], default='pending', max_length=20)),
                ('total_amount', models.IntegerField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('discountedrate', models.IntegerField(default=0)),
                ('totalcost', models.IntegerField(default=0)),
                ('orderdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('orderno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.product')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('sessionid', models.CharField(max_length=200)),
                ('discountedrate', models.IntegerField(default=0)),
                ('totalcost', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newshopapp.product')),
            ],
        ),
    ]