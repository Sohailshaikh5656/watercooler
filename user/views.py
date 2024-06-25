from django.shortcuts import render,redirect
from myadmin.models import *
from django.http import HttpResponse,HttpResponseBadRequest
from django.conf import settings
from django.core.mail import send_mail 
from .helper import send_forget_password_mail_to_agency
import os
from django.contrib import auth,messages
from django.contrib.auth.tokens import default_token_generator
from .utils import supplier_token_generator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User  # Ensure User model is imported
import razorpay
from watercooler.settings import ROZARPAY_API_KEY, ROZARPAY_API_SE_KEY
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .utils import render_to_pdf
from django.views.generic import View

my_order_id = None
my_payment_id = None

client = razorpay.Client(auth=(ROZARPAY_API_KEY, ROZARPAY_API_SE_KEY))

class GeneratePdf(View):
    def get(self,request,*args,**kwargs):
        id = request.session['order_id_recepit']
        result = Order.objects.get(pk=id)
        product = Product.objects.get(pk = result.product_id)
        cost = result.quantity*product.price
        user_info = User.objects.get(pk=result.user_id)
        user_profile = User_profile.objects.get(user_id = result.user_id)
        area = Area.objects.get(pk=user_profile.area)
        area = area.name
        city = City.objects.get(pk=user_profile.city)
        city = city.name
        
        
        global my_payment_id
        global my_order_id
        
        my_order_id = None
        my_payment_id = None

        
        context = {'result':result,'product':product,'cost':cost,'user_info':user_info,'user_profile':user_info,'user_profile':user_profile,'area':area,'city':city}
        pdf = render_to_pdf('user/receipt.html',context)
        return HttpResponse(pdf,content_type="application/pdf")




# Create your views here.
    
def user_profile(request):
    id = request.user.id
    if id == None:
        return redirect('/user/login')
    else:
        result = User_profile.objects.get(user_id=id)
        context = {'result':result}
        return render(request,"user/user_profile.html",context)
def edit_profile(request):
    id = request.user.id
    if id == None:
        return redirect('/user/login')
    else:
        result = User_profile.objects.get(user_id=id)
        cities = City.objects.all()
        area = Area.objects.all()
        context = {'cities':cities,'area':area,'result':result}
        return render(request,"user/edit_profile.html",context)
def Home(request):
    # Assuming Feedback has a ForeignKey to User
    feedback = Feedback.objects.select_related('user').all()  # Use select_related to optimize query
    product = Product.objects.all()
    context = {
        'feedback': feedback,
        'product':product
    }
    return render(request, 'user/index.html', context)


def Supplier_Register(request):
    cities = City.objects.all()
    context = {'cities':cities}
    return render(request,'user/SupplierRegister.html',context)

def Suppliers_Store(request):
    if request.method == 'POST':
        branchname = request.POST.get('branchname')
        ownername = request.POST.get('ownername')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        address = request.POST.get('address')
        city_id = request.POST.get('city')  # Get city ID from form
        area_id = request.POST.get('area')  # Get area ID from form
        
        # Fetch city and area objects from database
        city = City.objects.get(id=city_id)
        area = Area.objects.get(id=area_id)
        
        if password == cpassword:
            # If passwords match, create new Supplier object
            Suppliers.objects.create(
                branchname=branchname,
                ownername=ownername,
                email=email,
                phone=phone,
                password=password,
                address=address,
                city=city,
                area=area,
                stock=1,
                approval=0
            )
            request.session['register'] = True
        else:
            # If passwords don't match, set session variable for password mismatch
            request.session['password_mismatch'] = True

    # Redirect back to the registration page after processing the form
    return redirect("/user/Supplier_Register") 
def Suppliers_login(request):
    return render(request,'user/Suppliers_login.html',)

def Suppliers_Check(request):
    email1 = request.POST['email']
    password1 = request.POST['password']
    get = Suppliers.objects.filter(email=email1,password=password1,approval=1)

    if get.exists():  # Check if the query returned any results
        supplier = get.first()  # Get the first matching supplier
        request.session['supplier_id'] = supplier.id 
        return redirect('/suppliers/Dashboard')
    else:
        return HttpResponse("User Not Available")

def supplier_forget(request):
    context={}
    return render(request,'user/supplier_forget.html',context)


def supplier_forget_chk(request):
    email = request.POST['email']
    supplier = Suppliers.objects.get(email=email)
    supplier_id = supplier.id
    if supplier is None:
        return HttpResponse('Invalid Email or Supplier Not Available :')
    else:
        branch_name = supplier.branchname
        branch_owner = supplier.ownername
        request.session['supplier_id'] = supplier.id 
        token = supplier_token_generator(supplier)
        send_forget_password_mail_to_agency(email, branch_name, branch_owner, token)
        #messages.success(request, 'Check Your Mail ')
        return HttpResponse('Email Send :')
    
    
from django.shortcuts import render
from django.http import HttpResponseBadRequest

def changePassword(request):
    token = request.GET.get('token')
    if token:
        # Use the token parameter here
        print(token)  # Output the token for debugging
        # ... additional logic to handle the token ...
    else:
        # Handle the case where the token is not provided
        return HttpResponseBadRequest('Token is required')
    context = {}
    return render(request, 'user/changePassword.html', context)

def supplier_change_pass(request):
    id =  request.session['supplier_id']
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    if password == cpassword:
        result = Suppliers.objects.get(id=id)
        result.password = password
        result.save()
        return redirect('/user/Suppliers_login')
    else :
        return HttpResponse("Password Mis Match")

def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).all()
    return JsonResponse(list(areas.values('id', 'name')), safe=False)

def clear_message(request):
    if request.method == 'POST':
        if 'register' in request.session:
            del request.session['register']
        if 'password_mismatch' in request.session:
            del request.session['password_mismatch']
        if 'feedback' in request.session:
            del request.session['feedback']
        if 'feedback_updated' in request.session:
            del request.session['feedback_updated']
        if 'inquiry_send' in request.session:
            del request.session['inquiry_send']
        if 'order_done' in request.session:
            del request.session['order_done']
            
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


def User_Register(request):
    cities = City.objects.all()
    context = {'cities':cities}
    return render(request,'user/user_registration.html',context)

from django.db import IntegrityError
from django.contrib import auth,messages
def User_Store(request):
    if request.method == 'POST':
        FirstName = request.POST.get('fname')
        LastName = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        address = request.POST.get('address')
        city_id = request.POST.get('city')  # Get city ID from form
        area_id = request.POST.get('area')  # Get area ID from form
        
        # Fetch city and area objects from database
        city = City.objects.get(id=city_id)
        area = Area.objects.get(id=area_id)
        
        total_users = User.objects.count()
        username = email
        try: 
            if password != cpassword:
                request.session['password_mismatch'] = True
            # If passwords match, create new Supplier object
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already taken')
                return redirect('/user/register')
            
            else:
                result = User.objects.create_user(
                    first_name=FirstName,
                    last_name=LastName,
                    email=email,
                    password=password,
                    username=username
                )
                
                
                User_profile.objects.create(phone=phone,address=address,city=city,area=area,user_id=result.id)
                request.session['register'] = True
                return redirect ('/user/login')
                # If passwords don't match, set session variable for password mismatch
               
        except IntegrityError as e:
            messages.warning(request, 'Username already taken')
            return redirect('/user/register')

    # Redirect back to the registration page after processing the form
    return redirect("/user/Supplier_Register") 



def login(request):
    return render(request,'user/user_login.html')

def login_check(request):
    try:
        username = request.POST['email']
        password = request.POST['password']
        result1 = User.objects.get(username=username)
        result = auth.authenticate(request, username=username,password=password)
        if result1.first_name == "" or result1.is_staff != 0:
            messages.success(request, 'Invalid Username Or Password or You are Not Authorised User !!')
            print('Invalid Username Or Password or You are Not Authorised User')
            return redirect('/user')
        if result is None:
            messages.success(request, 'Invalid Username or Password')
            print('Invalid Username or Password')
            return redirect('/user/')
        else:
            auth.login(request, result)
            return redirect('/user/Home')

    except ObjectDoesNotExist:
         my_object = None
         messages.success(request, 'Invalid Username or not Found Username')
         print('Invalid Username or You are not Admin')
         return redirect('/user/')
     
def feedback(request):
    return render(request,'user/feedback.html')

def feedback_store(request):
    if request.user.is_authenticated:
        id = request.user.id
        rating = request.POST.get('star')
        message = request.POST.get('msg')

        if rating and message:
            data = {
                'rating': rating,
                'Message': message,
                'user_id': id
            }
            # Check if Feedback object exists for the user
            feedback_obj, created = Feedback.objects.update_or_create(user_id=id, defaults=data)
            
            if created:
                request.session['feedback'] = True
            else:
                request.session['feedback_updated'] = True
            
            return redirect('/user/feedback')
        else:
            return redirect('/user/feedback')  # Handle case where rating or message is missing
    else:
        return redirect('/user/login')  # Redirect to login if user is not authenticated    
def inquiry(request):
    return render(request,"user/contact.html")

def inquiry_store(request):
    name  = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    subject = request.POST['subject']
    message = request.POST['message']
    
    Inquiry.objects.create(name=name,email=email,phone=phone,subject=subject,Message=message)
    request.session['inquiry_send'] = True
    return redirect('/user/inquiry')



def viewmore(request,id):
    result = Product.objects.get(pk=id)
    context = {'result':result}
    return render(request,'user/shop.html',context)

def logout(request):
    auth.logout(request)
    return redirect('/user/login')   

def order_page(request,id):
    result = Product.objects.get(pk=id)
    request.session['order_id'] = id
    result1 = Suppliers.objects.filter(approval=1,stock=1).order_by('branchname')
    
    context = {'result':result,'result1':result1}
    return render(request,'user/order.html',context)
def order_store(request,id):
    qty = request.POST['qty']
    address = request.POST['address']
    order_receive_date = request.POST['order_rec']
    user_id = request.user.id
    supplier = request.POST['supplier']
    
    order_details = Order.objects.create(quantity=qty,order_address=address,order_deliver=order_receive_date,payment_id=" ",payments="None",product_id=id,supplier_id=supplier,user_id=user_id,approval=0)
    order_id = order_details.id
    request.session['order_id_recepit']=order_id
    request.session['Order_done'] = True
    redirect_url = f"/user/Payment/{order_id}"
    return redirect (redirect_url)

# def Payment(request):
#     context={}
#     return render(request,'user/payment.html',context)
    

def update_profile(request,id):
    
    result = User.objects.get(pk = id)
    result.first_name = request.POST['fname']
    result.last_name = request.POST['lname']
    result.email = request.POST['email']
    result.username = request.POST['email']
    result.save()
          
    result1 = User_profile.objects.get(user_id=id)
    result1.address = request.POST['address']
    result1.phone = request.POST['contact']
    result1.city = request.POST['city']
    result1.area = request.POST['area']
     

    result1.save()
    return redirect('/user/Home')
 

  # Import your Order model here

@csrf_exempt
def success(request):
    global my_order_id
    global my_payment_id
    if my_order_id!=None and my_payment_id!=None:
        order_id = my_order_id
        payment_order_id = my_payment_id
        result = Order.objects.get(pk=order_id)
        result.payment_id = payment_order_id
        result.payments = "Done"
        result.save()
        return render(request,'user/success.html')
    else : 
        return HttpResponse("Tav se Mil:")
def Payment(request,id):
    r = Order.objects.get(pk=id)
    qty = r.quantity
    r1 = Product.objects.get(pk=r.product_id)
    price = r1.price
    total_price = qty*price*100
    total = qty*price
    DATA = {
        "amount": total_price,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        },
        "payment_capture":1
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']
    global my_order_id
    global my_payment_id
    my_order_id = id
    my_payment_id = payment_order_id
    context={'price':price,'qty':qty,'total':total,'amount':DATA['amount'],'api_key':ROZARPAY_API_KEY,'order_id' : payment_order_id}
    
    return render(request,'user/payment.html',context)

    


