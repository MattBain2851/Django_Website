import datetime
from django.db import models
from django.utils import timezone
from django.utils.timezone import now

# Create your models here.


class ProfilePic(models.Model):
    pic = models.FileField(upload_to='profiles/',
                           default='profiles/anonymous.png')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pic.name


class Account(models.Model):
    # Base Account Fields
    account_first_name = models.CharField(max_length=30)
    account_last_name = models.CharField(max_length=30)
    account_phone_number = models.CharField(
        max_length=15, default='Not yet set')

    account_email = models.CharField(max_length=100)
    account_state_abbr = models.CharField(
        max_length=500, default='Not yet set')
    account_city = models.CharField(max_length=100, default='Not yet set')

    profile_pic = models.OneToOneField(ProfilePic,
                                       on_delete=models.CASCADE,
                                       primary_key=True,

                                       )

    # Driver Fields
    account_is_driver = models.BooleanField(default=False)
    driver_rating = models.IntegerField(default=-1)
    user_id = models.IntegerField(default=-1)

    # Shopping Fields
    shopping_list = models.ManyToManyField("ShoppingCart")
    order_list = models.ManyToManyField("Order")

    def __str__(self):
        return self.account_first_name + " " + self.account_last_name


class Order(models.Model):
    recipient_email = models.CharField(max_length=100, default="meme@meme.com")

    order_id = models.IntegerField(default=-1)
    driver_id = models.TextField(max_length=500, default="")

    time_of_order = models.DateTimeField('date published')

    # copying how it was done in the accounts
    item_list = models.ManyToManyField("ShoppingCart")

    # in case they have special notes
    notes = models.TextField(max_length=500, default="")

    delivery_address_PartA = models.TextField(max_length=500, default="")
    delivery_address_PartB = models.TextField(max_length=500, default="")
    delivery_address_City = models.TextField(max_length=500, default="")
    delivery_address_State = models.TextField(max_length=500, default="")
    delivery_address_ZIP = models.TextField(max_length=500, default="")

    status = models.TextField(max_length=10, default="unaccepted")

    def __str__(self):
        str = ""
        for x in self.item_list.all():
            str = str + " " + x.item_name
        return self.recipient_email + " | " + str


class Store(models.Model):
    # Example field up to be changed, remember to migrate database after changing models
    store_name = models.CharField(max_length=200)


class Suggestion(models.Model):
    Title = models.CharField(max_length=150)
    Text = models.TextField(max_length=1500)
    sub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.Text


class APISearch(models.Model):
    ItemName = models.CharField(max_length=150)

    def __str__(self):
        return self.ItemName


class ShoppingCart(models.Model):
    item_name = models.CharField(max_length=200)
    item_quantity = models.IntegerField(default=1)
    item_price = models.DecimalField(decimal_places=2, max_digits=100)
    item_picture = models.ImageField(
        upload_to=None, verbose_name='image', default='/shop/static/shop/images/fridge.png')

    def __str__(self):
        return self.item_name
