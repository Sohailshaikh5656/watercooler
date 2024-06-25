from django.shortcuts import render,redirect,HttpResponse
from myadmin.models import *
from django.core.mail import send_mail 
from .helper import send_forget_password_mail_to_agency
import os
from django.contrib import auth,messages
from django.contrib.auth.tokens import default_token_generator
from .utils import supplier_token_generator
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

def Dashboard(request):
    if  'supplier_id' in request.session :
        context = {}
        return render(request,'suppliers/index.html',context)
    else :
        return redirect('/user/Suppliers_login')
        
def logout(request):
    request.session.flush()  # Destroy all session data
    return redirect('/user/Suppliers_login') 
# Create your views here.
def manage_order(request):
     if  'supplier_id' in request.session :
         id = request.session['supplier_id']
         result = Order.objects.filter(supplier_id = id)
         context = {'result' : result}
         return render(request,"suppliers/manage_order.html",context)
     else:
         return redirect('/user/Suppliers_login')
def order_viewmore(request,id):
    result = Order.objects.get(pk=id)
    product = Product.objects.get(pk = result.product_id)
    cost = result.quantity*product.price
    user_info = User.objects.get(pk=result.user_id)
    user_profile = User_profile.objects.get(user_id = result.user_id)
    area = Area.objects.get(pk=user_profile.area)
    area = area.name
    city = City.objects.get(pk=user_profile.city)
    city = city.name
    context = {'result':result,'product':product,'cost':cost,'user_info':user_info,'user_profile':user_info,'user_profile':user_profile,'area':area,'city':city}
    return render(request,'suppliers/order_viewmore.html',context)
    
    
def approval(request,id):
    result = Order.objects.get(pk=id)
    result.approval=1
    result.save()
    product = Product.objects.get(pk=result.product_id)
    supplier = Suppliers.objects.get(pk=result.supplier_id)
    user = User.objects.get(pk=result.user_id)
    email = user.email
    
    order_id = result.id
    qty = result.quantity
    price = product.price
    supplier_phone = supplier.phone
    Total_price = result.quantity*product.price
    
    
    token = supplier_token_generator(result)
    send_forget_password_mail_to_agency(email, order_id, qty, price,supplier_phone,Total_price,token)
     #messages.success(request, 'Check Your Mail ')
    return HttpResponse('Email Send :')


def Receipt(request):
    token = request.GET.get('token')
    if token:
        # Use the token parameter here
        print(token)  # Output the token for debugging
        # ... additional logic to handle the token ...
    else:
        # Handle the case where the token is not provided
        return HttpResponseBadRequest('leo')
    context = {}
    return render(request, 'suppliers/Receipt.html', context)
