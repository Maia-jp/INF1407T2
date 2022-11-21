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

#Aux
import json
import uuid


#Home Page
def home(request):
    #User authenticated -> show user mainpage
    if request.user.is_authenticated:
        #User Authentication respose
        respose = userAuthPage(request)
        return respose
    else:    
        return redirect("login")

# Register page 
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




#
# User Functions
#
from django.http import QueryDict
def userAuthPage(request):
    #Any request
    userModel = User.objects.get(username=request.user.username)
    snippetsObj = Snippet.objects.filter(author=userModel).values_list('id','title','updated_at','lang') 
    userCodeIds = []
    print(snippetsObj)
    for id,title,dt,lang in snippetsObj:
        print(lang)
        userCodeIds.append([str(id),title,dt.strftime("%m/%d/%Y, %H:%M:%S"),lang])
    context = {
        'codeIDs': userCodeIds
    }

    #ajax requests
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    #DELETE
    if request.method == 'DELETE':
        if is_ajax:
            # Delete codeID
            qd = QueryDict(request.body)
            codeID = uuid.UUID(qd["codeID"])
            snippet = Snippet.objects.get(id=codeID)
            snippet.delete()
        
            #Respose
            response_data = {}
            response_data['status'] = 'ok'
            return HttpResponse(json.dumps(response_data))

    
    
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context,request))