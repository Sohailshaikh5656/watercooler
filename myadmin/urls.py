"""
URL configuration for watercooler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myadmin import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('Add_Category', views.Add_Category, name='Add_Category'),
    path('Store_Product',views.Store_Product,name='Store_Product'),
    path('clear_stored_message/', views.clear_stored_message, name='clear_stored_message'),
    path('showAllproduct',views.showAllproduct,name='showAllproduct'),
    path('productedit/<int:id>',views.productedit,name="productedit"),
    path('product_update/<int:id>',views.product_update,name="product_update"),
    path('product_delete/<int:id>',views.product_delete,name="product_delete"),
    path('Approve_Reject',views.Approve_Reject,name="Approve_Reject"),
    path('Approve/<int:id>',views.Approve,name="Approve"),
    path('reject/<int:id>',views.reject,name="reject"),
    path('showAllsuppliers',views.showAllsuppliers,name="showAllsuppliers"),
    path('viewmore_suppliers/<int:id>',views.viewmore_suppliers,name="viewmore_suppliers"),
    path('alluser',views.alluser,name="alluser"),
    path('viewmore_user/<int:id>',views.viewmore_user,name="viewmore_user"),
    path('user_delete/<int:id>',views.user_delete,name="user_delete"),
    path('allfeedback',views.allfeedback,name="allfeedback"),
    path('allinquiry',views.allinquiry,name="allinquiry"),
    path('inquiry_delete/<int:id>', views.inquiry_delete, name='inquiry_delete'),
    path('feedback_delete/<int:id>', views.feedback_delete, name='feedback_delete'),
    path('login', views.login, name='login'),
    path('login_chk', views.login_chk, name='login_chk'),
    path('logout', views.logout, name='logout'),
    

    
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)