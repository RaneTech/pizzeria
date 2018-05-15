from django.shortcuts import render
from pizzas.models import Pizza,Topping
from pizzas.forms import PizzaForm,ToppingForm
from django.urls import reverse
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
	return render(request,'pizzas/index.html')

@login_required
def pizzas(request):
	pizzas = Pizza.objects.filter(maker=request.user).order_by('name')
	context = {'pizzas': pizzas}
	return render(request,'pizzas/pizzas.html', context)

@login_required
def pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
#	if pizza.maker != request.user:
#		raise Http404
	check_pizza_maker(request,pizza)
	toppings = pizza.topping_set.order_by('-name')
	context = {'pizza': pizza, 'toppings': toppings}
	return render(request,'pizzas/pizza.html', context)

@login_required
def new_pizza(request):
	if request.method != 'POST':
		form = PizzaForm()
	else:
		form = PizzaForm(request.POST)
		if form.is_valid():
			new_pizza = form.save(commit=False)
			new_pizza.maker = request.user
			new_pizza.save()
			return HttpResponseRedirect(reverse('pizzas'))
	
	context = {'form': form}
	return render(request, 'pizzas/new_pizza.html', context)

@login_required
def edit_pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	if pizza.maker != request.user:
		raise Http404
	if request.method != 'POST':
		form = PizzaForm(instance=pizza)
	else:
		form = PizzaForm(instance=pizza,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('pizzas'))
	
	context = {'pizza':pizza, 'form':form}
	return render(request, 'pizzas/edit_pizza.html', context)

@login_required
def del_pizza(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	if pizza.maker != request.user:
		raise Http404
	pizza.delete()
	return HttpResponseRedirect(reverse('pizzas'))


@login_required
def new_topping(request,pizza_id):
	pizza = Pizza.objects.get(id=pizza_id)
	if pizza.maker != request.user:
		raise Http404
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

@login_required
def edit_topping(request,topping_id):
	topping = Topping.objects.get(id=topping_id)
	pizza = topping.pizza
	if pizza.maker != request.user:
		raise Http404
	if request.method != 'POST':
		form = ToppingForm(instance=topping)
	else:
		form = ToppingForm(instance=topping,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('pizza',args=[pizza.id]))
	
	context = {'topping':topping, 'pizza':pizza, 'form':form}
	return render(request, 'pizzas/edit_topping.html', context)

@login_required
def del_topping(request,topping_id):
	topping = Topping.objects.get(id=topping_id)
	pizza = topping.pizza
	if pizza.maker != request.user:
		raise Http404
	topping.delete()
	return HttpResponseRedirect(reverse('pizza',args=[pizza.id]))



def check_pizza_maker(request,pizza):
	"""check pizza maker"""
	if pizza.maker != request.user:
		raise Http404













