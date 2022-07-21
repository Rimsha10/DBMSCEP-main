#Programmer Defined
#____________IMPORTS_________________
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponseRedirect 
from .models.category import Category
from .models.customer import Customer
from .models.product import Product
from .models.contact import Contact
from .models.order import Order
from .models.order_Items import OrderItem
from .models.shippingAddress import ShippingAdress
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime



#____________HOME____________________
def index(request):
    categories=Category.get_all_categories()
    products=Product.get_all_products()
    context = {'products':products,'categories':categories}
    return render(request,'index.html',context)
#____________ABOUT____________________
def about(request):
    return render(request,'about.html')
#____________CONTACT____________________
def contact(request):
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        contact.name=name
        contact.email=email
        contact.phone=phone
        contact.message=message
        contact.save()
        messages.success(request,'Your response has been submitted succesfully!')
        return redirect('contact')
    return render(request,'contact.html')
#__________PRODUCTSPART_________________
def products(request):
    prds=None
    categories=Category.get_all_categories()
    categoryID=request.GET.get('category')
    if categoryID:
        prds=Product.get_all_products_by_categoryid(categoryID)
       
    else:
        prds=Product.get_all_products()
    data={'products':prds,'categories':categories}
    return render(request,"products.html",data)


#________________ProductsDetails___________________
def product_detail(request,id):
    productdet=Product.objects.get(id=id)
    return render(request,'product_detail.html',{'data':productdet})

class EditProfile(View):
  def get(self, request):
    context = {}
    active_customer=request.session.get('customer')
    data=Customer.get_customer(str(active_customer))
    context["data"]=data
    return render(request, 'edit_profile.html',context)
  def post(self,request):
    context = {}
    active_customer=request.session.get('customer')
    data=Customer.get_customer(str(active_customer))
    context["data"]=data    
    if request.method=="POST":
        fn = request.POST.get("first_name")
        ln = request.POST.get("last_name")
        em = request.POST.get("email")
        con = request.POST.get("phone")
        password=request.POST.get("password")
        data.first_name = fn
        data.last_name = ln
        data.email = em
        data.phone = con
        data.password= password
        sp=Signup()
        error_message = sp.validateCustomer(data)

        if not error_message:
            print(fn, ln, con, em, password)
            data.password = make_password(data.password)
            data.save()
            return redirect('index')
        else:
            context = {
                'error': error_message,
                'values': data
            }
            return render(request, 'edit_profile.html', context)

    return render(request,"edit_profile.html",context)
#______________Register__________________________
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message



#___________________________________Login_______________________________________
class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')
#_____profile_______________
class Profile(View):
    def get(self,request):
        active_customer=request.session.get('customer')
        print(request.session.get('customer'))
        cus=Customer.get_customer(str(active_customer))
        return render(request,'profile.html',{'customer':cus})
#___________Cart____________
def cart(request):
    #____if user is authenticated____
    if request.user.is_authenticated:
        active_customer= request.session.get('customer')
        customer = Customer.get_customer(str(active_customer))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    #___if user isnt authenticated_______
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    context={'items': items, 'order': order }
    return render(request, 'cart.html', context)

#______________checkout___________
def checkout(request):
    if request.user.is_authenticated:
        active_customer= request.session.get('customer')
        customer = Customer.get_customer(str(active_customer))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    #___create empty cart for now for non logged in user_______
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        items=[]
    
    context={'items': items, 'order': order }
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    active_customer= request.session.get('customer')
    customer = Customer.get_customer(str(active_customer))
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        active_customer= request.session.get('customer')
        customer = Customer.get_customer(str(active_customer))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id


        if total == order.get_cart_total:
            order.complete = True
        order.save()
        ShippingAdress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )

    else:
        print('user not logged in')
    
    return JsonResponse('Payment Complete', safe=False)




