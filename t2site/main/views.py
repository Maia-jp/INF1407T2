from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#Models
from django.contrib.auth.models import User
from snippet.models import Snippet

#Home Page
def home(request):
    if request.user.is_authenticated:
        userModel = User.objects.get(username=request.user.username)
        snippetsObj = Snippet.objects.filter(author=userModel).values_list('id','updated_at') 
        userCodeIds = []
        print(snippetsObj)
        for id,dt in snippetsObj:
            userCodeIds.append([str(id),dt.strftime("%m/%d/%Y, %H:%M:%S")])
        context = {
            'codeIDs': userCodeIds
        }
        
        template = loader.get_template('home.html')
        return HttpResponse(template.render(context,request))
    else:    
        return redirect("login")


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect("login")
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)