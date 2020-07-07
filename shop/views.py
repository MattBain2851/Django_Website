from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.contrib.auth import logout
import datetime
from django.contrib.auth.models import User
import requests
import urllib.parse
from .forms import APITestForm, SuggestionFormForm, ProfilePicForm
from .models import Suggestion, Account, ShoppingCart, Order, ProfilePic
from datetime import datetime
from random import randint


def LandingView(request):
    return render(request, 'shop/landingpage.html')

# TODO: Possible citaion?
# https://stackoverflow.com/questions/14529815/logout-with-django-social-auth
# Logs user out and redirects to the landing page


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('shop:landing'))


def LoginView(request):
    # Check if a first time user. If so send to T&C else to profile
    if datetime.now().timestamp() <= request.user.date_joined.timestamp() + 2:
        user = request.user
        pic = ProfilePic()
        pic.save()
        newAccount = Account(account_first_name=user.first_name,
                             account_last_name=user.last_name,
                             account_phone_number="Not yet set",
                             account_email=user.email,
                             user_id=randint(0, 100000),
                             profile_pic=pic,
                             )
        newAccount.save()
        return HttpResponseRedirect(reverse('shop:termsConditions'))
    else:
        return HttpResponseRedirect(reverse('shop:landing'))


def AccountProfile(request):
    user = request.user
    userAccount = Account.objects.get(account_email=user.email)
    userOrders = userAccount.order_list
    # if userAccount.account_is_driver:
    made_order_list = Order.objects.filter(recipient_email=user.email)

    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            recent = ProfilePic.objects.all().order_by('-uploaded_at')
            Account.objects.filter(account_email=user.email).update(profile_pic=recent[0])
    form = ProfilePicForm
    userAccount = Account.objects.get(account_email=user.email)
    return render(request, 'shop/accountProfile.html', {
        'made_order_list': made_order_list,
        'order_list': userOrders.all(),
        'form': form,
        'fileName': "/media/" + userAccount.profile_pic.pic.name,
    })


def SuggestionList(request):
    latest_suggestion_list = Suggestion.objects.order_by('-sub_date')[:5]
    template = loader.get_template('shop/SuggestionList.html')
    context = {
        'latest_suggestion_list': latest_suggestion_list,
    }
    return HttpResponse(template.render(context, request))


def SuggestionDetail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    return render(request, 'shop/suggestionDetail.html', {'suggestion': suggestion})


def SuggestionForm(request):

    if request.method == "POST":
        form = SuggestionFormForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sug_name = form.cleaned_data['Title']
            post.body_text = form.cleaned_data['Text']
            post.sub_date = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('shop:suggestion'))
    else:
        form = SuggestionFormForm()
        return render(request, 'shop/suggestionForm.html', {'form': form})


def CartAdd(request):
    user = request.user
    userAccount = Account.objects.get(account_email=user.email)
    userCart = userAccount.shopping_list
    item_name_s = request.POST.get('item_name')
    item_price_s = request.POST.get('item_price')
    item_picture_s = request.POST.get('item_picture')

    if len(userCart.filter(item_name=item_name_s)) == 0:
        new_item_i = ShoppingCart(
            item_name=item_name_s, item_price=item_price_s, item_quantity=1, item_picture=item_picture_s)
        new_item_i.save()
        userCart.add(new_item_i)

    else:
        """ for i in ShoppingCart.objects.filter(item_name=item_name_s):
            i.item_quantity += 1
            i.save() """
        for i in userCart.all():
            if i.item_name == item_name_s:
                i.item_quantity += 1
                i.save()

    # new_item.save()
    return HttpResponseRedirect(reverse('shop:store'))


def StoreView(request):
    if request.method == "POST":
        form = APITestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.ItemName = form.cleaned_data['ItemName']
            post.save()
            return HttpResponseRedirect(reverse('shop:store_result'))
    else:
        # trying something wild I am really sorry I spent an hour trying to get the loop to work if the project wasn't due literally Monday I would try harder
        s1 = "Almond Milk Vanilla"
        # &term=Eggs&perPage=15&categoryId=1-32806
        urlAtt = dict()
        urlAtt['api_key'] = "870d8ebca2624b13a3391218fc61eb11"
        urlAtt['publisherId'] = "TEST"
        urlAtt['locale'] = "en_US"
        urlAtt['site'] = "shop"
        urlAtt['shipCountry'] = "US"
        urlAtt['perPage'] = "1"
        urlAtt['categoryId'] = "1-32806"
        if (s1 != ''):
            urlAtt['term'] = s1
        else:
            s1 = "None Given"

        if (len(urlAtt) != 0):
            response = requests.get(
                'https://api2.shop.com/AffiliatePublisherNetwork/v2/products?' + urllib.parse.urlencode(urlAtt,
                                                                                                        doseq=True))
            productData = response.json()
        else:
            response = requests.get(
                'https://images-api.nasa.gov/search?q=OkayCanWePleaseEnterSomeSearchTerms')
            productData = response.json()

        s2 = "Cheese"
        # &term=Eggs&perPage=15&categoryId=1-32806
        urlAtt2 = dict()
        urlAtt2['api_key'] = "870d8ebca2624b13a3391218fc61eb11"
        urlAtt2['publisherId'] = "TEST"
        urlAtt2['locale'] = "en_US"
        urlAtt2['site'] = "shop"
        urlAtt2['shipCountry'] = "US"
        urlAtt2['perPage'] = "1"
        urlAtt2['categoryId'] = "1-32806"
        if (s2 != ''):
            urlAtt2['term'] = s2
        else:
            s2 = "None Given"

        if (len(urlAtt2) != 0):
            response2 = requests.get(
                'https://api2.shop.com/AffiliatePublisherNetwork/v2/products?' + urllib.parse.urlencode(urlAtt2,
                                                                                                        doseq=True))
            productData2 = response2.json()
        else:
            response2 = requests.get(
                'https://images-api.nasa.gov/search?q=OkayCanWePleaseEnterSomeSearchTerms')
            productData2 = response2.json()

        s3 = "Crackers"
        # &term=Eggs&perPage=15&categoryId=1-32806
        urlAtt3 = dict()
        urlAtt3['api_key'] = "870d8ebca2624b13a3391218fc61eb11"
        urlAtt3['publisherId'] = "TEST"
        urlAtt3['locale'] = "en_US"
        urlAtt3['site'] = "shop"
        urlAtt3['shipCountry'] = "US"
        urlAtt3['perPage'] = "1"
        urlAtt3['categoryId'] = "1-32806"
        if (s3 != ''):
            urlAtt3['term'] = s3
        else:
            s3 = "None Given"

        if (len(urlAtt3) != 0):
            response3 = requests.get(
                'https://api2.shop.com/AffiliatePublisherNetwork/v2/products?' + urllib.parse.urlencode(urlAtt3,
                                                                                                        doseq=True))
            productData3 = response3.json()
        else:
            response3 = requests.get(
                'https://images-api.nasa.gov/search?q=OkayCanWePleaseEnterSomeSearchTerms')
            productData3 = response3.json()
        items = list()
        items = productData['products']
        items2 = (productData2['products'])
        items3 = productData3['products']
        form = APITestForm()
        return render(request, 'shop/SearchPage.html', {'form': form, 'items': items, 'items2': items2, 'items3': items3})


def StoreResultView(request):
    if request.method == 'GET':
        form = APITestForm()
        # create a form instance and populate it with data from the request:
       # form = APITestForm(request.GET)
        # check whether it's valid:
        # if form.is_valid():
            #s1 = form.cleaned_data.get('ItemName')
        s1 = request.GET.get("ItemName")
        # &term=Eggs&perPage=15&categoryId=1-32806
        urlAtt = dict()
        urlAtt['api_key'] = "870d8ebca2624b13a3391218fc61eb11"
        urlAtt['publisherId'] = "TEST"
        urlAtt['locale'] = "en_US"
        urlAtt['site'] = "shop"
        urlAtt['shipCountry'] = "US"
        urlAtt['perPage'] = "20"
        urlAtt['categoryId'] = "1-32806"
        if (s1 != ''):
            urlAtt['term'] = s1
        else:
            s1 = "None Given"

        if (len(urlAtt) != 0):
            response = requests.get(
                'https://api2.shop.com/AffiliatePublisherNetwork/v2/products?' + urllib.parse.urlencode(urlAtt, doseq=True))
            productData = response.json()
        else:
            response = requests.get(
                'https://images-api.nasa.gov/search?q=OkayCanWePleaseEnterSomeSearchTerms')
            productData = response.json()

        items = list()
        items = productData['products']

        return render(request, 'shop/Store.html', {'form':form ,'Items': items})


def TermsConditions(request):
    return render(request, 'shop/termsconditions.html')


def CartView(request):

    user = request.user
    if user.is_authenticated:
        shopping_list = ShoppingCart.objects.order_by('item_name')

        is_remove = request.POST.get('is_remove')
        item_name_str = request.POST.get('item_name')
        item_qt = request.POST.get('item_quantity')
        is_remove_all = request.POST.get('is_remove_all')
        is_remove_ev = request.POST.get('is_remove_everything')
        add_it = request.POST.get('add_item')

        userAccount = Account.objects.get(account_email=user.email)
        userCart = userAccount.shopping_list
        displayCart = userAccount.shopping_list.order_by('item_name')

        if is_remove == "a":
            if int(item_qt) <= 1:
                """  removeItem = ShoppingCart.objects.filter(item_name=item_name_str)
                ShoppingCart.objects.filter(item_name=item_name_str).delete() """
                for i in userCart.all():
                    if i.item_name == item_name_str:
                        userCart.remove(i)
                is_remove = False
            else:
                """ for i in ShoppingCart.objects.filter(item_name=item_name_str):
                    i.item_quantity -= 1
                    i.save() """
                for i in userCart.all():
                    if i.item_name == item_name_str:
                        i.item_quantity -= 1
                        i.save()

        elif is_remove_all == "a":
            """ ShoppingCart.objects.filter(item_name=item_name_str).delete() """
            for i in userCart.all():
                if i.item_name == item_name_str:
                    userCart.remove(i)
            is_remove_all = False
        elif is_remove_ev == "a":
            for i in userCart.all():
                userCart.remove(i)
            is_remove_ev = False
        elif add_it == "a":
            """ for i in ShoppingCart.objects.filter(item_name=item_name_str):
                i.item_quantity += 1
                i.save() """
            for i in userCart.all():
                if i.item_name == item_name_str:
                    i.item_quantity += 1
                    i.save()

        template = loader.get_template('shop/Cart.html')
        context = {
            'shopping_list': displayCart,
        }
    else:
        template = loader.get_template('shop/Cart.html')
        context = {}
    return HttpResponse(template.render(context, request))

# this is what is called when the "submit order" button is pressed


def PersonalOrderAdd(request):
    user = request.user
    userAccount = Account.objects.get(account_email=user.email)

    # TODO: (LOW PRIORITY) Switch this over to running on ID's not notes
    order_id = request.POST.get('order_id')
    status_s = request.POST.get('status')

    Order.objects.filter(order_id=order_id).update(status="inprogress")
    passedOrder = Order.objects.get(order_id=order_id)
    userOrders = userAccount.order_list

    userOrders.add(passedOrder)
    return HttpResponseRedirect(reverse('shop:personal_orders'))

# this is what displays the orders in a list


def PersonalOrderView(request):
    user = request.user
    if user.is_authenticated:
        is_remove = request.POST.get('is_remove')
        is_remove_ev = request.POST.get('is_remove_everything')
        order_id = request.POST.get('order_id')
        userAccount = Account.objects.get(account_email=user.email)
        userOrders = userAccount.order_list
        order_list = userOrders.all()
        for item in order_list.all():
            print(item)

        if is_remove_ev == "a":
            for i in userOrders.all():
                order = Order.objects.filter(
                    order_id=i.order_id).update(status="unaccepted")

        if is_remove_ev == "c":
            for i in userOrders.all():
                order = Order.objects.filter(
                    order_id=i.order_id).update(status="completed")

        if is_remove == "a":
            order = Order.objects.filter(
                order_id=order_id).update(status="unaccepted")

        if is_remove == "k":
            Order.objects.get(order_id=order_id).delete()
            user = request.user
            userAccount = Account.objects.get(account_email=user.email)
            userOrders = userAccount.order_list
            # if userAccount.account_is_driver:
            made_order_list = Order.objects.filter(recipient_email=user.email)

            return render(request, 'shop/accountProfile.html', {
                'made_order_list': made_order_list,
                'order_list': userOrders.all(),
            })
        if is_remove == "q":
            Order.objects.get(order_id=order_id).delete()
            user = request.user
            userAccount = Account.objects.get(account_email=user.email)
            userOrders = userAccount.order_list
            order_list = Order.objects.filter(
                status="unaccepted").order_by('time_of_order')
            template = loader.get_template('shop/Order.html')
            context = {
                'order_list': order_list
            }
            return HttpResponse(template.render(context, request))

        if is_remove == "c":
            order = Order.objects.filter(
                order_id=order_id).update(status="completed")

        template = loader.get_template('shop/PersonalOrders.html')
        context = {
            'order_list': userOrders.filter(status="inprogress"),
        }
    else:
        template = loader.get_template('shop/PersonalOrders.html')
        context = {}
    if(userOrders.filter(status="inprogress").count() != 0):
        return HttpResponse(template.render(context, request))
    else:
        order_list = Order.objects.filter(
            status="unaccepted").order_by('time_of_order')
        template = loader.get_template('shop/Order.html')
        context = {
            'order_list': order_list
        }
        return HttpResponse(template.render(context, request))


def OrderView(request):
    # Only filters unaccepted orders and sorts by most oldest first
    order_list = Order.objects.filter(
        status="unaccepted").order_by('time_of_order')
    template = loader.get_template('shop/Order.html')
    context = {
        'order_list': order_list
    }
    return HttpResponse(template.render(context, request))

# this is what is displaying the order form


def OrderForm(request):
    user = request.user
    if user.is_authenticated:
        shopping_list = ShoppingCart.objects.order_by('item_name')
        template = loader.get_template('shop/OrderForm.html')

        userAccount = Account.objects.get(account_email=user.email)
        userCart = userAccount.shopping_list

        context = {
            'shopping_list': userCart.all(),
        }

    else:
        template = loader.get_template('shop/OrderForm.html')
        context = {}
    return HttpResponse(template.render(context, request))

  #  return render(request, 'shop/OrderForm.html')


def OrderAdd(request):
    notes_s = request.POST.get('notes')
    delivery_address_PartA_s = request.POST.get('delivery_address_PartA')
    delivery_address_PartB_s = request.POST.get('delivery_address_PartB')
    delivery_address_City_s = request.POST.get('delivery_address_City')
    delivery_address_State_s = request.POST.get('delivery_address_State')
    delivery_address_ZIP_s = request.POST.get('delivery_address_ZIP')
    order_id_s = randint(0, 10000000)
    user = request.user
    userAccount = Account.objects.get(account_email=user.email)
    driver_id_s = userAccount.user_id
    item_list_s = request.POST.get('item_list')
    email = request.POST.get('recipient_email')
    status = "unaccepted"
    #time_of_order_s = datetime.now()
    new_item_i = Order(
        recipient_email=email,
        order_id=order_id_s,
        driver_id=driver_id_s,
        time_of_order=timezone.now(),
        # item_list
        notes=notes_s,
        delivery_address_PartA=delivery_address_PartA_s,
        delivery_address_PartB=delivery_address_PartB_s,
        delivery_address_City=delivery_address_City_s,
        delivery_address_State=delivery_address_State_s,
        delivery_address_ZIP=delivery_address_ZIP_s,
        status=status
    )

    new_item_i.save()

    user = request.user
    userAccount = Account.objects.get(account_email=user.email)
    userFirstName = userAccount.account_first_name
    userShoppingList = userAccount.shopping_list

    for x in userShoppingList.all():
        new_item_i.item_list.add(x)
    for x in userShoppingList.all():
        userShoppingList.remove(x)

    return HttpResponseRedirect(reverse('shop:thankyou'))


def ThankYouView(request):
    return render(request, 'shop/ThankYou.html')
