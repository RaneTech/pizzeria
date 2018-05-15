from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))
	

def register(request):
	if request.method != 'POST':
		myform = UserCreationForm()
	else:
		myform = UserCreationForm(request.POST)
		if myform.is_valid():
			new_user = myform.save()
			authenticated_user = authenticate(username=new_user.username,
			  password=request.POST['password1'])
#zhe ge xing bu tong
#			  password=new_user.password)
			login(request,authenticated_user)
			return HttpResponseRedirect(reverse('index'))
	
	context = {'form': myform}
	return render(request, 'chief/register.html', context)





















