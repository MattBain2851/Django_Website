# Generated by Django 2.2.7 on 2019-11-25 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APISearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(default='profiles/anonymous.png', upload_to='profiles/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('item_quantity', models.IntegerField(default=1)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('item_picture', models.ImageField(default='/shop/static/shop/images/fridge.png', upload_to=None, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=150)),
                ('Text', models.TextField(max_length=1500)),
                ('sub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_email', models.CharField(default='meme@meme.com', max_length=100)),
                ('order_id', models.IntegerField(default=-1)),
                ('driver_id', models.TextField(default='', max_length=500)),
                ('time_of_order', models.DateTimeField(verbose_name='date published')),
                ('notes', models.TextField(default='', max_length=500)),
                ('delivery_address_PartA', models.TextField(default='', max_length=500)),
                ('delivery_address_PartB', models.TextField(default='', max_length=500)),
                ('delivery_address_City', models.TextField(default='', max_length=500)),
                ('delivery_address_State', models.TextField(default='', max_length=500)),
                ('delivery_address_ZIP', models.TextField(default='', max_length=500)),
                ('status', models.TextField(default='unaccepted', max_length=10)),
                ('item_list', models.ManyToManyField(to='shop.ShoppingCart')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_first_name', models.CharField(max_length=30)),
                ('account_last_name', models.CharField(max_length=30)),
                ('account_phone_number', models.CharField(default='Not yet set', max_length=15)),
                ('account_email', models.CharField(max_length=100)),
                ('account_state_abbr', models.CharField(default='Not yet set', max_length=500)),
                ('account_city', models.CharField(default='Not yet set', max_length=100)),
                ('profile_pic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shop.ProfilePic')),
                ('account_is_driver', models.BooleanField(default=False)),
                ('driver_rating', models.IntegerField(default=-1)),
                ('user_id', models.IntegerField(default=-1)),
                ('order_list', models.ManyToManyField(to='shop.Order')),
                ('shopping_list', models.ManyToManyField(to='shop.ShoppingCart')),
            ],
        ),
    ]
