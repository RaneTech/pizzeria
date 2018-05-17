from django.shortcuts import render,get_object_or_404
from pizzas.models import Pizza,Topping
from pizzas.forms import PizzaForm,ToppingForm
from django.urls import reverse
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
	return render(request,'pizzas/index.html')


def pizzas(request):
	pizzas = Pizza.objects.filter(public='True').order_by('name')
	context = {'pizzas': pizzas}
	return render(request, 'pizzas/pizzas.html', context)
	
@login_required
def my_pizzas(request):
	pizzas = Pizza.objects.filter(maker=request.user).order_by('name')
	context = {'pizzas': pizzas}
	return render(request, 'pizzas/my_pizzas.html', context)


def pizza(request,pizza_id):
	pizza = get_object_or_404(Pizza, id=pizza_id)
	flag = False
	if pizza.public == False:
		if pizza.maker != request.user:
			raise Http404
	else:
		if pizza.maker == request.user:
			flag = True
						
	toppings = pizza.topping_set.order_by('-name')
	context = {'pizza': pizza, 'toppings': toppings, 'flag':flag }
	return render(request,'pizzas/pizza.html', context)

@login_required
def new_pizza(request):
	if request.method != 'POST':
		form = PizzaForm()
	else:
		form = PizzaForm(request.POST)
		check_public = request.POST.getlist('check_public')
		if form.is_valid():
			new_pizza = form.save(commit=False)
			new_pizza.maker = request.user
			if check_public[0] == '1':
				new_pizza.public = True
			new_pizza.save()
			return HttpResponseRedirect(reverse('pizzas'))
	
	context = {'form': form}
	return render(request, 'pizzas/new_pizza.html', context)

@login_required
def edit_pizza(request,pizza_id):
	pizza = get_object_or_404(Pizza, id=pizza_id)
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
	pizza = get_object_or_404(Pizza, id=pizza_id)
	if pizza.maker != request.user:
		raise Http404
	pizza.delete()
	return HttpResponseRedirect(reverse('pizzas'))


@login_required
def new_topping(request,pizza_id):
	pizza = get_object_or_404(Pizza, id=pizza_id)
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
	topping = get_object_or_404(Topping, id=topping_id)
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
	topping = get_object_or_404(Topping, id=topping_id)
	pizza = topping.pizza
	if pizza.maker != request.user:
		raise Http404
	topping.delete()
	return HttpResponseRedirect(reverse('pizza',args=[pizza.id]))



def check_pizza_maker(request,pizza):
	"""check pizza maker"""
	if pizza.maker != request.user:
		raise Http404












