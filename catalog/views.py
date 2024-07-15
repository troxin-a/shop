from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from catalog.models import Contacts, Product


def index(request):
    products = Product.objects.order_by("-id")

    context = {
        "title": "Аптека-лека ГЛАВНАЯ",
        "objects_list": products,
    }
    return render(request, "catalog/index.html", context)


def detail(request, pk):
    product = Product.objects.get(pk=pk)
    title = f"Аптека-лека: {product}"

    context = {
        "title": title,
        "product": product,
    }
    return render(request, "catalog/detail.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("text")
        print(name, email, text, sep="\n")

        return HttpResponseRedirect(reverse("catalog:index"))

    contacts = Contacts.objects.all()

    context = {
        "title": "Аптека-лека КОНТАКТЫ",
        "contacts": contacts,
    }
    return render(request, "catalog/contacts.html", context)
