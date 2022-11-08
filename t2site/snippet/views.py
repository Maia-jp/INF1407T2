import uuid
from plistlib import UID
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#Models
from django.contrib.auth.models import User
from snippet.models import ProgLang
from snippet.models import Snippet

def index(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())


def new(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            user = User.objects.get(username=request.user.username)
            code = request.POST['snippet']
            lang = ProgLang.objects.get(name=request.POST['lang'])
            print([user,code,lang])
            newSnippet = Snippet(author=user,code=code,lang=lang)
            newSnippet.save()
            return HttpResponseRedirect("/snippet/{}".format(newSnippet.id))

        programmingLangs  = ProgLang.objects.all().values()
        context = {'progLang':programmingLangs}

        template = loader.get_template('create.html')
        return HttpResponse(template.render(context,request))
    else:    
        return redirect("login")


def snippetTemplate(request, id):
    id = uuid.UUID(id)
    code = Snippet.objects.get(id=id)
    return HttpResponse(code.code)