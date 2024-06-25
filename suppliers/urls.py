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
from suppliers import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('manage_order', views.manage_order, name='manage_order'),
    # path('Store_Product',views.Store_Product,name='Store_Product'),
    # path('clear_stored_message/', views.clear_stored_message, name='clear_stored_message'),
    # path('showAllproduct',views.showAllproduct,name='showAllproduct'),
    # path('productedit/<int:id>',views.productedit,name="productedit"),
    path('order_viewmore/<int:id>',views.order_viewmore,name="order_viewmore"),
    path('approval/<int:id>',views.approval,name="approval"),
    path('Receipt/', views.Receipt, name='Receipt'),
    
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)