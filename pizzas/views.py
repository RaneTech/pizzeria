from django.shortcuts import render
from pizzas.models import Pizza,Topping
from pizzas.forms import PizzaForm,ToppingForm
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
	return render(request,'pizzas/index.html')

def pizzas(request):
	pizzas = Pizza.objects.order_by('name')
	context = {'pizzas': pizzas}
	return render(request,'pizzas/pizzas.html', context)

def pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	toppings = pizza.topping_set.order_by('-name')
	context = {'pizza': pizza, 'toppings': toppings}
	return render(request,'pizzas/pizza.html', context)

def new_pizza(request):
	if request.method != 'POST':
		form = PizzaForm()
	else:
		form = PizzaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('pizzas'))
	
	context = {'form': form}
	return render(request, 'pizzas/new_pizza.html', context)

def edit_pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	if request.method != 'POST':
		form = PizzaForm(instance=pizza)
	else:
		form = PizzaForm(instance=pizza,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('pizzas'))
	
	context = {'pizza':pizza, 'form':form}
	return render(request, 'pizzas/edit_pizza.html', context)

def del_pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	pizza.delete()
	return HttpResponseRedirect(reverse('pizzas'))


def new_topping(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	if request.method != 'POST':
		form = ToppingForm()
	else:
		form = ToppingForm(request.POST)
		if form.is_valid():
			new_topping = form.save(commit=False)
			new_topping.pizza = pizza
			new_topping.save()
			return HttpResponseRedirect(reverse('pizza',args=[pizza_id]))
	
	context = {'pizza':pizza, 'form':form}
	return render(request, 'pizzas/new_topping.html', context)

def edit_topping(request,topping_id):
	topping = Topping.objects.get(id=topping_id)
	pizza = topping.pizza
	if request.method != 'POST':
		form = ToppingForm(instance=topping)
	else:
		form = ToppingForm(instance=topping,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('pizza',args=[pizza.id]))
	
	context = {'topping':topping, 'pizza':pizza, 'form':form}
	return render(request, 'pizzas/edit_topping.html', context)

def del_topping(request,topping_id):
	topping = Topping.objects.get(id=topping_id)
	pizza = topping.pizza
	topping.delete()
	return HttpResponseRedirect(reverse('pizza',args=[pizza.id]))

















