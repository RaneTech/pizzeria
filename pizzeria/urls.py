"""pizzeria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import login
from pizzas import views 
from chief import views as chief_views


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.index, name='index'),
	path('pizzas/', views.pizzas, name='pizzas'),
	path('my_pizzas/', views.my_pizzas, name='my_pizzas'),
	path('pizzas/<pizza_id>/', views.pizza, name='pizza'),
	path('new_pizza/', views.new_pizza, name='new_pizza'),
	path('edit_pizza/<pizza_id>/', views.edit_pizza, name='edit_pizza'),
	path('del_pizza/<pizza_id>/', views.del_pizza, name='del_pizza'),
	path('new_topping/<pizza_id>/', views.new_topping, name='new_topping'),
	path('del_topping/<topping_id>/', views.del_topping, name='del_topping'),
	path('edit_topping/<topping_id>/', views.edit_topping, name='edit_topping'),
	path('login/', login, {'template_name':'chief/login.html'}, name='login'),
	path('logout/', chief_views.logout_view, name='logout'),
	path('register/', chief_views.register, name='register'),
	
	
]
