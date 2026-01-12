# -------------------------
# CLEAN IMPORTS AT THE TOP
# -------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from stores.models import Store
import uuid


# -------------------------
# SELLER DASHBOARD
# -------------------------
@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return render(request, "not_authorized.html")

    products = Product.objects.filter(seller=request.user)

    return render(request, "products/seller_dashboard.html", {
        "products": products
    })


# -------------------------
# ADD PRODUCT
# -------------------------
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        form.fields['store'].queryset = Store.objects.filter(owner=request.user)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.sku = uuid.uuid4().hex[:10]
            product.save()
            return redirect("seller_dashboard")
    else:
        form = ProductForm()
        form.fields['store'].queryset = Store.objects.filter(owner=request.user)

    return render(request, "products/add_product.html", {"form": form})


# -------------------------
# EDIT PRODUCT
# -------------------------
@login_required
def edit_product(request, product_id):
    if not request.user.is_seller:
        return render(request, "products/not_authorized.html")

    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("seller_dashboard")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/edit_product.html", {"form": form})


# -------------------------
# DELETE PRODUCT
# -------------------------
@login_required
def delete_product(request, product_id):
    if not request.user.is_seller:
        return render(request, "products/not_authorized.html")

    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()

    return redirect("seller_dashboard")


# -------------------------
# PUBLIC PRODUCT LIST + DETAIL
# -------------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})