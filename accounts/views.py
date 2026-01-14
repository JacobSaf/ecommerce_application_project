from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from orders.models import Cart

from .forms import CustomUserRegistrationForm


# -------------------------
# REGISTER VIEW
# -------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = CustomUserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.is_seller:
                return redirect("seller_dashboard")
            else:
                return redirect("buyer_dashboard")  # <-- FIXED

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "accounts/login.html")


# -------------------------
# LOGOUT VIEW
# -------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def buyer_dashboard(request):
    # Prevent sellers from accessing buyer pages
    if request.user.is_seller:
        return redirect("seller_dashboard") # seller cannot access buyer dash

    # Load the actual cart for this user
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    items = cart.items.select_related("product")

    return render(
        request,
        "accounts/buyer_dashboard.html",
        {"cart": cart, "items": items}
    )



