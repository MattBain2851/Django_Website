import datetime
from django.test import TestCase, Client, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from shop.models import ProfilePic, Order, Store, Suggestion, APISearch, ShoppingCart, Account
from django.http import HttpRequest

from django.contrib.auth.models import User
from django.contrib.auth import logout, get_user, user_logged_in, user_logged_out

# Note: In the testing plan I had laid out an elaborate scheme of MBCC testing.
# This proved to be out of the scope of this project. I am currently in 3250
# software testing and so I got a bit overexcited when tasked with designing
# our testing philosophy. Like all good testing, it is important to find a
# balance between cost of writing/running tests and correctness of code.
# This assignment is much more geared towards creating an awesome website
# rather than the thoroughness of the tests. The actual writing of the code
# took more time than I had expected so our focus was not on meeting heavy
# test requirements. Because we had a round of beta testing, we were able
# to adequately sniff out any bugs with our software so we feel confident
# that our product is tested enough and the balance between cost of developing
# our tests and effectiveness of them is in a good place.


class SuggestionStrTestCase(TestCase):
    def setUp(self):
        Suggestion.objects.create(
            Title="Test title", Text="Test text", sub_date=datetime.datetime.now())

    def test_str_function(self):
        test_suggestion = Suggestion.objects.get(Title="Test title")
        self.assertEqual(test_suggestion.__str__(), "Test text")
        self.assertNotEqual(test_suggestion.__str__(), "Test title")


class APISearchTestCase(TestCase):
    def setUp(self):
        APISearch.objects.create(ItemName="eggs")

    def test_str_function(self):
        test_search = APISearch.objects.get(ItemName="eggs")
        self.assertEqual(test_search.__str__(), "eggs")
        self.assertNotEqual(test_search.__str__(), "not eggs")


class ShoppingCartRemoveItem(TestCase):
    def setUp(self):
        ShoppingCart.objects.create(item_name = "Banana",  item_price = 4.50, item_quantity = 2 )
    def test_str_function(self):
        test_suggestion = ShoppingCart.objects.get(item_name="Banana")
        test_suggestion.item_quantity -= 1
        test_suggestion.save()
        self.assertEqual(test_suggestion.item_quantity, 1)


class ShoppingCartAddItem(TestCase):
    def setUp(self):
        ShoppingCart.objects.create(item_name = "Banana",  item_price = 4.50, item_quantity = 2 )
    def test_str_function(self):
        test_suggestion = ShoppingCart.objects.get(item_name="Banana")
        test_suggestion.item_quantity += 1
        test_suggestion.save()
        self.assertEqual(test_suggestion.item_quantity, 3)


class ShoppingCartTestPrice(TestCase):
    def setUp(self):
        ShoppingCart.objects.create(item_name = "Banana",  item_price = 4.50, item_quantity = 2 )
    def test_str_function(self):
        test_suggestion = ShoppingCart.objects.get(item_name="Banana")
        test_suggestion.save()
        self.assertEqual(test_suggestion.item_price, 4.50)


class ShoppingCartTestName(TestCase):
    def setUp(self):
        ShoppingCart.objects.create(item_name = "Banana",  item_price = 4.50, item_quantity = 2 )
    def test_str_function(self):
        test_suggestion = ShoppingCart.objects.get(item_name="Banana")
        test_suggestion.save()
        self.assertEqual(test_suggestion.item_name, "Banana")


class AccountStrTestCase(TestCase):
    def setUp(self):
        pic = ProfilePic()
        pic.save()
        Account.objects.create(account_first_name="Test first", account_last_name="Test last", account_email="a@gmail.com",
                               account_state_abbr="VA", account_city="Charlottesville", account_is_driver=False, profile_pic=pic)

    def test_str_function(self):
        test_account = Account.objects.get(account_first_name="Test first")
        self.assertEqual(test_account.__str__(), "Test first Test last")
        self.assertNotEqual(test_account.__str__(), "Test title")


class ShoppingCartStrTestCase(TestCase):
    def setUp(self):
        ShoppingCart.objects.create(item_name="Test name", item_price="1", item_quantity="6")
    def test_str_function(self):
        test_cart = ShoppingCart.objects.get(item_name="Test name")
        self.assertEqual(test_cart.__str__(), "Test name")
        self.assertNotEqual(test_cart.__str__(), "1")


class AdminTest(LiveServerTestCase):

    def setUp(self):
        User.objects.create_user('D', 'gmail@gmail.com', 'P')

    def test_login(self):

        login = self.client.login(username='D', password='P')
        self.assertTrue(login)
        self.assertTrue(user_logged_in)

'''
    def test_cart_list(self):

        response = self.client.get(reverse('shop:cart'))
        self.assertContains(response, 'Oops!', status_code=200)
        self.assertTemplateUsed(response, 'shop/Cart.html')
'''


class OrderModelTest(TestCase):
     def setUp(self):
        Order.objects.create(time_of_order=timezone.now())
        
        Order.objects.create(order_id=300, driver_id="Howdy", time_of_order=timezone.now(), notes="I want this", delivery_address_PartA="Hogwarts", delivery_address_PartB="Rice Hall", delivery_address_City="Charlottesville", delivery_address_State="Virginia", delivery_address_ZIP="23805")
        
        
     def testGeneric1(self):
        generic_order = Order.objects.get(notes="")
        self.assertEqual(generic_order.order_id, -1)
     
     def testGeneric2(self):
        generic_order = Order.objects.get(notes="")
        self.assertEqual(generic_order.notes, "")
        
     def testGeneric3(self):
        generic_order = Order.objects.get(notes="")
        self.assertEqual(generic_order.delivery_address_State, "")
        
     def testExample1(self):
        example_order = Order.objects.get(notes="I want this")
        self.assertEqual(example_order.order_id, 300)
        
     def testExample2(self):
        example_order = Order.objects.get(notes="I want this")
        self.assertEqual(example_order.driver_id, "Howdy")
        
     #Tests to make sure strings are modifiable
        
     def testExample3(self):
        example_order = Order.objects.get(notes="I want this")
        self.assertEqual(example_order.delivery_address_PartA + example_order.delivery_address_PartB, "HogwartsRice Hall")
        
     #Tests to make sure values are being set
        
     def testExample4(self):
        example_order = Order.objects.get(notes="I want this")
        self.assertNotEqual(example_order.notes, "")
        
     def test_modify_example(self):
        example_order = Order.objects.get(notes="I want this")
        example_order.order_id = 299
        example_order.save()
        self.assertEqual(example_order.order_id, 299)

     def status_test(self):
        example_order = Order.objects.get("I want this")
        example_order.status = "inprogress"
        example_order.save()
        self.assertEqual(example_order.status, "inprogress")
        
        
class AccountModelTests(TestCase):
    def setUp(self):
        pic = ProfilePic()
        pic.save()
        pic1 = ProfilePic()
        pic1.save()
        pic2 = ProfilePic()
        pic2.save()
        Account.objects.create(account_email="generic@generic.com", account_first_name="Generic", account_last_name="Test", profile_pic=pic)
        Account.objects.create(account_email="more@values.com", account_first_name="More", account_last_name="Values", account_phone_number="9999999999", account_state_abbr="VA", account_city="Charlottesville", profile_pic=pic1)
        Account.objects.create(account_email="driver@drives.com", account_first_name="Driver", account_last_name="Test",
                               account_phone_number="1111111111", account_state_abbr="VA",
                               account_city="Charlottesville", account_is_driver=True, driver_rating=5, profile_pic=pic2)

    def testDriver1(self):
        driver_account = Account.objects.get(account_email="driver@drives.com")
        self.assertEqual(driver_account.account_phone_number,"1111111111")

    def testDriver2(self):
        driver_account = Account.objects.get(account_email="driver@drives.com")
        self.assertEqual(driver_account.account_first_name,"Driver")

    def testDriver3(self):
        driver_account = Account.objects.get(account_email="driver@drives.com")
        self.assertEqual(driver_account.account_last_name,"Test")

    def testDriver4(self):
        driver_account = Account.objects.get(account_email="driver@drives.com")
        self.assertEqual(driver_account.account_is_driver,True)

    def testDriver5(self):
        driver_account = Account.objects.get(account_email="driver@drives.com")
        self.assertEqual(driver_account.driver_rating,5)

    def testGeneric1(self):
        generic_account = Account.objects.get(account_email="generic@generic.com")
        self.assertEqual(generic_account.account_is_driver,False)

    def testGeneric2(self):
        generic_account = Account.objects.get(account_email="generic@generic.com")
        self.assertEqual(generic_account.account_first_name,"Generic")

    def testGeneric3(self):
        generic_account = Account.objects.get(account_email="generic@generic.com")
        self.assertEqual(generic_account.account_city,"Not yet set")

    def testGeneric4(self):
        generic_account = Account.objects.get(account_email="generic@generic.com")
        self.assertEqual(generic_account.account_phone_number,"Not yet set")

    def testGeneric5(self):
        generic_account = Account.objects.get(account_email="generic@generic.com")
        self.assertEqual(generic_account.driver_rating,-1)

    def testMore1(self):
        more_account = Account.objects.get(account_email="more@values.com")
        self.assertEqual(more_account.driver_rating,-1)

    def testMore2(self):
        more_account = Account.objects.get(account_email="more@values.com")
        self.assertEqual(more_account.account_phone_number,"9999999999")

    def testMore3(self):
        more_account = Account.objects.get(account_email="more@values.com")
        self.assertEqual(more_account.account_last_name,"Values")

    def testMore4(self):
        more_account = Account.objects.get(account_email="more@values.com")
        self.assertEqual(more_account.account_first_name,"More")

    def testMore5(self):
        more_account = Account.objects.get(account_email="more@values.com")
        self.assertEqual(more_account.account_state_abbr,"VA")