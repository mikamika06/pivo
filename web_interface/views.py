from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from monitoring.models import Product
from .forms import ProductForm


def product_list_view(request):
    products = Product.objects.select_related('product_type', 'store').all()
    context = {
        'products': products
    }
    return render(request, 'web_interface/product_list.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'web_interface/product_detail.html', context)


def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" successfully created')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form': form
    }
    return render(request, 'web_interface/product_form.html', context)


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" successfully updated')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'web_interface/product_form.html', context)


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" successfully deleted')
        return redirect('product_list')
    
    context = {
        'product': product
    }
    return render(request, 'web_interface/product_detail.html', context)

def external_products_list_view(request):
    products = Product.objects.select_related('product_type', 'store').all()
    
    context = {
        'products': products,
    }
    
    return render(request, 'web_interface/external_products_list.html', context)


def external_product_delete_view(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        messages.success(request, f'Продукт "{product_name}" успішно видалено з каталогу')
    
    return redirect('external_products_list')


