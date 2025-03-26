from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.timezone import now

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.items.filter
        cartItems = order.get_total_cart_items
        user_not_login = "none"
        user_login = "block"
    else:
        items = []
        order = {'getCartItems': 0, 'getCartTotal': 0}
        cartItems = order['getCartItems']
        user_not_login = "block"
        user_login = "none"
    products = Product.objects.all()
    context= {'products': products, 'user_not_login': user_not_login, 'user_login': user_login, 'cartItems': cartItems}
    return render(request, "app/home.html", context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete=False)
        items = order.items.all() 
        all_selected = all(item.choiced for item in items)
        cartItems = order.get_total_cart_items
        user_not_login = "none"
        user_login = "block"
    else:
        order = None
        items = []
        cartItems = order['getCartItems']
        all_selected = False 
        user_not_login = "block"
        user_login = "none"
    context= {'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login, 'cartItems': cartItems, 'all_selected': all_selected}
    return render(request, "app/cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.items.filter(choiced=True)
        cartItems = order.get_total_cart_items
        user_not_login = "none"
        user_login = "block"
    else:
        items = []
        order = {'getCartItems': 0, 'getCartTotal': 0}
        cartItems = order['getCartItems']
        user_not_login = "block"
        user_login = "none"
    context = {'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login, 'cartItems': cartItems}
    return render(request, "app/checkout.html", context)

#View for search action
def searchView(request):
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains=searched)
    else:
        searched = ""
        keys = []

    # Truyền các biến trạng thái đăng nhập
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.items.filter
        cartItems = order.get_total_cart_items
        user_not_login = "none"
        user_login = "block"
    else:
        items = []
        order = {'getCartItems': 0, 'getCartTotal': 0}
        cartItems = order['getCartItems']
        user_not_login = "block"
        user_login = "none"

    context = {
        "searched": searched,
        "keys": keys,
        "user_login": user_login,
        "user_not_login": user_not_login,
        'cartItems': cartItems
    }
    return render(request, 'app/search.html', context)


#Login Sign in page
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(1)
        print(form.is_valid())
        if form.is_valid():
            print(1)
            form.save()
            return redirect('login')
    context = {'form': form, 'user_not_login': "block", 'user_login': "none"}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password not correct!!!')

    context = {'user_not_login': "block", 'user_login': "none"}
    return render(request, 'app/login.html', context)

# Logout
def logoutPage(request):
    logout(request)
    return redirect('login')

# Update Item
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, create = OrderItem.objects.get_or_create(order = order, product= product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove' and orderItem.quantity > 1:
        orderItem.quantity -= 1
    if action == 'select':
        orderItem.choiced = True
    elif action == 'unselect':
        orderItem.choiced = False
    orderItem.save()
    return JsonResponse('added', safe=False)


def delete_selected_items(request):
    data = json.loads(request.body)
    product_ids = data.get('productIds', [])

    customer = request.user
    order = Order.objects.get(customer=customer, complete=False)

    # Xóa các sản phẩm được chọn
    order.items.filter(product__id__in=product_ids, choiced=True).delete()

    return JsonResponse({'status': 'success'}, safe=False)

def shipping(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user

        # Tạo order mới
        old_order = Order.objects.get(customer=user, complete=False)
        new_order = Order.objects.create(
            customer=user,
            complete=True,
            transaction_id=f"{now().timestamp()}",
        )

        # Di chuyển các OrderItem đã chọn (choiced=True) từ order cũ sang order mới
        for item in old_order.items.filter(choiced=True):
            item.order = new_order
            item.save()

        # Tạo ShippingAddress
        ShippingAddress.objects.create(
            customer=user,
            order=new_order,
            reci_name=data["reci_name"],
            reci_phone=data["reci_phone"],
            address=data["address"],
            city=data["city"],
            province=data["province"],
            date_added=now(),
        )

        # Trả về phản hồi thành công
        return JsonResponse({"message": "Thanh toán thành công!"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)

# Product-detail
def productDetail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.items.filter
        cartItems = order.get_total_cart_items
        user_not_login = "none"
        user_login = "block"
    else:
        items = []
        order = {'getCartItems': 0, 'getCartTotal': 0}
        cartItems = order['getCartItems']
        user_not_login = "block"
        user_login = "none"

    context = {
        'product': product,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'cartItems': cartItems
    }
    return render(request, 'app/productdetail.html', context)