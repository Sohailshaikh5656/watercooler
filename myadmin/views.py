from django.shortcuts import render,redirect
from myadmin.models import *
from django.contrib import auth,messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def Dashboard(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        admin = User.objects.get(id=id)
        context = {'admin':admin}
        return render(request,'admin/index.html',context)
        


def showAllproduct(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = Product.objects.all()
        context = {'result':result}
        return render(request,'admin/showallproduct.html',context)
    

def Add_Category(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        water_capacity_options = list(range(1, 16))
        return render(request,'admin/form.html',{'water_capacity':water_capacity_options})

def Store_Product(request):
    productname = request.POST['productname']
    capacity = request.POST['Capacity']
    myfile = request.FILES['file']
    price = request.POST['price']
    description = request.POST['desc']
    

    mylocation = os.path.join(settings.MEDIA_ROOT,'uploads')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myfile.name, myfile)
    name = "uploads/"+myfile.name


    Product.objects.create(productname=productname,capacity=capacity,price=price,description=description,image=name)
    request.session['Stored'] = 'Data Stored !'
    return redirect('/myadmin/Add_Category')

@csrf_exempt
def clear_stored_message(request):
    if request.method == 'POST':
        request.session['Stored'] = None
        request.session['user_delete'] = None
        request.session['Store'] = None
        request.session['feedback_delete'] = None
        request.session['inquiry_delete'] = None
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
    
def productedit(request,id):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = Product.objects.get(pk=id)
        water_capacity_options = list(range(1, 16))
        demo = []
        for i in water_capacity_options:
            i = str(i)+" Liter"
            demo.append(i)
        context = {'result':result,'water_capacity':demo}
        return render(request,'admin/productedit.html',context)


def product_update(request,id):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        myfile = request.FILES['file']
        mylocation = os.path.join(settings.MEDIA_ROOT,'upload')
        obj = FileSystemStorage(location=mylocation)
        obj.save(myfile.name, myfile)

        data = {
                'productname': request.POST['productname'],
                'capacity': request.POST['Capacity'],
                'price': request.POST['price'],
                'description' : request.POST['desc'],
                'file' : myfile.name

            }

        Product.objects.update_or_create(pk=id, defaults=data)
        request.session['Store'] = 'Product Updated !'
        return redirect('/myadmin/showAllproduct')

def product_delete(request,id):
    result = Product.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/showAllproduct')



def Approve_Reject(request):
    result = Suppliers.objects.filter(approval=0)
    context = {'result':result}
    return render(request,'admin/app_rej.html',context)


def Approve(request,id):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        Supplier = Suppliers.objects.get(pk=id)
        Supplier.approval = True
        Supplier.save()
        return redirect('/myadmin/showAllsuppliers')

def reject(request,id):
    result = Suppliers.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/Approve_Reject')
    
def showAllsuppliers(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = Suppliers.objects.filter(approval=1)
        context = {'result':result}
        return render(request,'admin/showallsuppliers.html',context)

def viewmore_suppliers(request,id):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = Suppliers.objects.get(pk=id)
        context = {'result':result}
        return render(request,'admin/viewmore_suppliers.html',context)
        
def alluser(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = User.objects.filter(first_name__isnull=False).exclude(first_name__exact="")
    
        context = {'result':result}
        return render(request,'admin/alluser.html',context)
        
def viewmore_user(request,id):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = User_profile.objects.get(user_id=id)
        context = {'result':result}
        return render(request,'admin/viewmore_user.html',context)

def user_delete(request,id):
    result = User.objects.get(pk=id)
    result.delete()
    request.session["user_delete"]=True
    return redirect("/myadmin/alluser")

def allinquiry(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
        result = Inquiry.objects.all()
        context = {'result':result}
        return render(request,'admin/allinquiry.html',context)


def allfeedback(request):
    id = request.user.id
    if id == None:
        return redirect('/myadmin/login')
    else:
    
        result = Feedback.objects.all()
        context = {'result':result}
        return render(request,'admin/allfeedback.html',context)

def feedback_delete(request,id):
    result = Feedback.objects.get(pk=id)
    result.delete()
    request.session['feedback_delete'] = True
    return redirect('/myadmin/allfeedback')

def inquiry_delete(request,id):
    result = Inquiry.objects.get(pk=id)
    result.delete()
    request.session['inquiry_delete'] = True
    return redirect('/myadmin/allinquiry')
        
        
def login(request):
    return render(request,'admin/signin.html')

def login_chk(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        result1 = User.objects.get(username=username)
        result = auth.authenticate(request, username=username,password=password)
        if result1.is_staff == 0:
            messages.success(request, 'Invalid Username Or Password or You are Not Authorised User !!')
            print('Invalid Username Or Password or You are Not Authorised User')
            return redirect('/myadmin/login')
        if result is None:
            messages.success(request, 'Invalid Username or Password')
            print('Invalid Username or Password')
            return redirect('/myadmin/login')
        else:
            auth.login(request, result)
            request.session['admin'] = result1.id
            return redirect('/myadmin/Dashboard')

    except ObjectDoesNotExist:
         my_object = None
         messages.success(request, 'Invalid Username or not Found Username')
         print('Invalid Username or You are not Admin')
         return redirect('/user/')
     
def logout(request):
    auth.logout(request)
    return redirect('/myadmin/login')   