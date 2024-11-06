# reviews/views.py
from django.shortcuts import render, get_object_or_404
from .models import Review

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    # Lógica para crear una nueva reseña
    return render(request, 'reviews/review_form.html')
