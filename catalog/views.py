import os
from config.settings import MEDIA_ROOT
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from catalog.models import Category, Contacts, Product


def index(request):
    page_number = request.GET.get("page", 1)

    products = Product.objects.order_by("-id")

    paginator = Paginator(products, 8)
    current_page = paginator.page(page_number)

    context = {
        "title": "Аптека-лека ГЛАВНАЯ",
        "objects_list": current_page,
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


def handle_uploaded_file(f):
    file_path = os.path.join(MEDIA_ROOT, Product.image.field.upload_to, f.name)

    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def add_product(request):
    if request.method == "POST":
        category = Category.objects.get(pk=request.POST.get("category"))
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price", 0)
        image = request.FILES.get("image")

        Product.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            image=image,
        )

        if image:
            handle_uploaded_file(request.FILES.get("image"))
        return redirect("catalog:detail", Product.objects.all().last().pk)

    categories = Category.objects.all()

    context = {
        "title": "Добавление продукта",
        "categories": categories,
    }
    return render(request, "catalog/add.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("text")
        print(name, email, text, sep="\n")

        return redirect("catalog:index")

    contacts = Contacts.objects.all()

    context = {
        "title": "Аптека-лека КОНТАКТЫ",
        "contacts": contacts,
    }
    return render(request, "catalog/contacts.html", context)
