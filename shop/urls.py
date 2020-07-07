from django.urls import path  # its friday mi amigos
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.LandingView, name='landing'),
    path('accounts/termsconditions/',
         views.TermsConditions, name='termsConditions'),

    path('accounts/profile/', views.AccountProfile, name='accountProfile'),
    path('accounts/login/', views.LoginView, name='login'),
    path('accounts/logout/', views.LogoutView, name='logout'),

    path('suggestion/list/', views.SuggestionList, name='suggestion'),
    path('suggestion/<int:pk>/', views.SuggestionDetail, name='suggestionDetail'),
    path('suggestion/', views.SuggestionForm, name='suggestionForm'),
    path('cart/list', views.CartView, name='cart'),
    path('cart/', views.CartAdd, name='cartadd'),
    # path('add_to_cart/', views.CartAdd, name='cart_add'),
    path('cart/list', views.CartView, name='cart'),

    path('Store/', views.StoreView, name='store'),
    path('Store/Result', views.StoreResultView, name='store_result'),
    path('orders/', views.OrderView, name="orders"),
    path('orderadd/', views.OrderAdd, name="orderadd"),
    path('orderForm', views.OrderForm, name='orderform'),
    path('PersonalOrderAdd/', views.PersonalOrderAdd, name="personal_order_add"),
    path('PersonalOrder/', views.PersonalOrderView, name="personal_orders"),

    path('ThankYou/', views.ThankYouView, name="thankyou")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
