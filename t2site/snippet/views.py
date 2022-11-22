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

# Models
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
            title = request.POST['snippetTitle']
            code = request.POST['snippet']
            lang = ProgLang.objects.get(name=request.POST['lang'])
            print([user, code, lang, title])
            newSnippet = Snippet(author=user, code=code,
                                 lang=lang, title=title)
            newSnippet.save()
            return HttpResponse("{}".format(newSnippet.id))
            # return HttpResponseRedirect("/snippet/{}".format(newSnippet.id))

        programmingLangs = ProgLang.objects.all().values()
        context = {'progLang': programmingLangs}

        template = loader.get_template('create.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect("login")


def snippetTemplate(request, id):
    id = uuid.UUID(id)
    obj = Snippet.objects.get(id=id)

    context = {
        "code": obj.code,
        "author": obj.author.username,
        "title": obj.title,
        "date": obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
        "edit": request.user.username == obj.author.username,
        "lang": obj.lang_id
    }

    template = loader.get_template('snippet.html')
    return HttpResponse(template.render(context, request))


def snippetEdit(request, id):
    id = uuid.UUID(id)
    codeSnippet = Snippet.objects.get(id=id)

    if request.user.is_authenticated:
        if request.user.username != codeSnippet.author.username:
            return HttpResponse("Sem permissao para alterar esse snippet")

        if request.method == "POST":
            return snippetEditPost(request)
        else:
            respose = snippetEditLoadPage(request, id, codeSnippet)
            return respose
    else:
        return redirect("login")


def snippetEditLoadPage(request, id, codeSnippet):
    context = {
        "id": id,
        "code": codeSnippet.code,
        "author": codeSnippet.author.username,
        "title": codeSnippet.title,
        "date": codeSnippet.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
        "lang": codeSnippet.lang_id
    }

    template = loader.get_template('edit.html')
    return HttpResponse(template.render(context, request))


def snippetEditPost(request):
    id_inPost = request.POST['id']
    code = request.POST['snippet']

    id = uuid.UUID(id_inPost)
    Snippet.objects.filter(id=id).update(code=code)

    return HttpResponse(id_inPost)
