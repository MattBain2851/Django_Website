from django.contrib import admin

from .models import Account, Order, Store, Suggestion, ShoppingCart, Order, ProfilePic


# class AccountInline(admin.TabularInline):
#    model = Account
#    extra = 3


admin.site.register(Account)
admin.site.register(Store)
admin.site.register(Suggestion)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(ProfilePic)
