from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    context = {
        "title": "Аптека-лека ГЛАВНАЯ",
    }
    return render(request, "catalog/index.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("text")
        print(name, email, text, sep="\n")

        return HttpResponseRedirect(reverse('catalog:index'))

    context = {
        "title": "Аптека-лека КОНТАКТЫ",
    }
    return render(request, "catalog/contacts.html", context)
