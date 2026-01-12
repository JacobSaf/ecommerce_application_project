from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm 

# Create your views here.
@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    store.delete()
    return redirect("store_list")


@login_required
def store_list(request):
    stores = Store.objects.filter(owner=request.user)
    return render(request, "stores/store_list.html", {"stores": stores})


@login_required
def create_store(request):
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            return redirect("store_list")
    else:
        form = StoreForm()

    return render(request, "stores/create_store.html", {"form": form})


@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect("store_list")
    else:
        form = StoreForm(instance=store)

    return render(request, "stores/edit_store.html", {"form": form, "store": store})
