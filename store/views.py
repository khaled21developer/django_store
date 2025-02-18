from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import Product, Slider, Category, Cart
from django.shortcuts import render, redirect
from .forms import SupportRequestForm
from django.contrib import messages


def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return render(
        request, 'index.html',
        {
            'products': products,
            'slides': slides
        }
    )


def product(request, pid):
    model = Product.objects.get(pk=pid)
    return render(
        request, 'product.html',
        {
            'product': model
        }
    )


def category(request, cid=None):
    cat = None

    cid = request.GET.get('category', cid)

    where = {}
    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'category.html', {
            'page_obj': page_obj,
            'category': cat
        }
    )


def cart(request):
    return render(
        request, 'cart.html'
    )


def cart_update(request, pid):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[pid])
    elif pid not in cart_model.items:
        cart_model.items.append(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been added to your cart.'),
        'items_count': len(cart_model.items)
    })


def cart_remove(request, pid):
    session_id = request.session.session_key

    if not session_id:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        return JsonResponse({})
    elif pid in cart_model.items:
        cart_model.items.remove(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been removed from your cart.'),
        'items_count': len(cart_model.items)
    })


def checkout(request):
    return render(
        request, 'checkout.html'
    )


def checkout_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()
    return render(
        request, 'checkout-complete.html'
    )


def support_request(request):
    if request.method == 'POST':
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'تم إرسال الرسالة بنجاح!'})
        else:
            error_messages = form.errors.as_json()  # تحويل الأخطاء إلى JSON
            return JsonResponse({'success': False, 'errors': error_messages}, status=400)

    form = SupportRequestForm()
    return render(request, 'support_request.html', {'form': form})

