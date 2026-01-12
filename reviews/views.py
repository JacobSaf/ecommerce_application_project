from django.shortcuts import get_object_or_404, redirect, render
from .models import Review
from .forms import ReviewForm
from products.models import Product
from orders.models import OrderItem


# Create your views here.
def leave_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product

            # Determine if verified
            purchased = OrderItem.objects.filter(
                order__user=request.user,
                product=product
            ).exists()

            review.verified = purchased
            review.save()

            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, "reviews/leave_review.html", {"form": form, "product": product})
