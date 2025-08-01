from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from vendor.models import Vendor
from menu.models import Category, Fooditem
from .models import Cart
from .context_processors import get_cart_counter
# Create your views here.

def marketPlace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active =True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = Fooditem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                # check if item is already added to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #increase cart quantity
                    checkCart.quantity +=1
                    checkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased cart quantity', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})
                except:
                    checkcart = Cart.objects.get(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added food to the cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})

            except:
                return JsonResponse({'status': 'failure', 'message': 'Food item is not available'})
        
        else:
            return JsonResponse({'status': 'failure', 'message': 'Invalid request'})


    else:
        return JsonResponse({'status': 'Login required!', 'message': 'please login to continue'})
    

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                # check if item is already added to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #decrease cart quantity
                    if checkCart.quantity > 1:
                        checkCart.quantity -=1
                        checkCart.save()

                    else:
                        checkCart.delete()
                        checkCart.quantity = 0

                    
                    return JsonResponse({'status': 'success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})
                except:
                
                    return JsonResponse({'status': 'failure', 'message': 'You do not have this item in the cart!'})

            except:
                return JsonResponse({'status': 'failure', 'message': 'Food item is not available'})
        
        else:
            return JsonResponse({'status': 'failure', 'message': 'Invalid request'})


    else:
        return JsonResponse({'status': 'Login required!', 'message': 'please login to continue'})
    

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'Cart item deleted!', 'cart_counter': get_cart_counter(request)})
            except:
                return JsonResponse({'status': 'failure', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Invalid request'})


                

