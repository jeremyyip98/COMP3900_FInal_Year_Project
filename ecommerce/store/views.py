from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseNotFound
import json

# Create your views here.
from .forms import OrderForm, CreateUserForm, UpdateUserForm, UpdateUserProfilePic

def store(request):

	if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def signup(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		form = CreateUserForm()
		if request.method == "POST":
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')

				messages.success(request, 'Account was created for ' + username)

				# create customer here
				customer = Customer()
				customer.user = user
				customer.nickname = user.username
				customer.email = user.email
				customer.save()

				template = render_to_string('store/email_template.html', {'name': user.username, 'username': user.username})

				print(settings.EMAIL_HOST_USER)
				email = EmailMessage(
					'You have successfully signed up for Petiverse!',
					template,
					settings.EMAIL_HOST_USER,
					[user.email],
				)

				email.fail_silently = False
				email.send()

				return redirect('signup_success')

	cartItems = 0
	context = {'form':form, 'cartItems':cartItems}
	return render(request, 'store/signup.html', context)

def signup_success(request):

	context = {}
	return render(request, 'store/signup_success.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('store')
			else:
				messages.info(request, 'Username OR password is incorrect')
	
	order = {'get_cart_total':0, 'get_cart_items':0}
	cartItems = 0
	context = {'cartItems':cartItems}
	return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def product_page(request, slug=None):
	
	product_filter = Product.objects.filter(slug_str=slug)
	if product_filter.count() != 1:
		return HttpResponseNotFound("404: Product listing was not found")
	product = product_filter.first()

	
	context = {"product": product, "tags": product.tags.names()}
	return render(request, 'store/product_description.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order.get('get_cart_items')

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def purchase_history(request):
	if not request.user.is_authenticated:
		return redirect('login')

	customer = request.user.customer
	# order is for cart to update the total number of items in cart
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orders = Order.objects.filter(customer=customer)
	order_items = OrderItem.objects.filter(order__in=orders).order_by('-date_added')

	purchases = []
	for item in order_items:
		purchases.append({
			"name": item.product.name,
			"seller": item.product.seller,
			"quantity": item.quantity,
			"date_added": item.date_added,
			"image": item.product.imageURL,
			"price": item.get_total
		})
	print(orders)
	cartItems = order.get_cart_items
	context = {"purchases": purchases, 'cartItems':cartItems}
	return render(request, 'store/purchase_history.html', context)
	
def wishlist(request):
	context = {}
	return render(request, 'store/wishlist.html', context)

# watchlist is a list of auction items that user watch to see
def watchList(request):
	context = {}
	return render(request, 'store/watchList.html', context)

def userProfile(request):
	if request.method == 'POST':
		user_form = UpdateUserForm(request.POST, instance=request.user.customer)
		user_pic_form = UpdateUserProfilePic(request.POST, request.FILES, instance=request.user.customer)
		if user_form.is_valid() and user_pic_form.is_valid():
			user_form.save()
			user_pic_form.save()
			messages.success(request, f'Your account information has been updated!')
			return redirect('user_profile')
	else:
		user_form = UpdateUserForm(instance=request.user.customer)
		user_pic_form = UpdateUserProfilePic(instance=request.user.customer)
	
	orders = request.user.customer.order_set.all()
	# Please don't delete the next three lines 
	# order is for cart to update the total number of items in cart
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	cartItems = order.get_cart_items

	orders = Order.objects.filter(customer=customer)

	context = {
		'user_form': user_form,
		'user_pic_form': user_pic_form,
		'orders': orders,
		'cartItems':cartItems
		}
	return render(request, 'store/user_profile.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	# Still have enough stock available
	if product.remaining_unit == 0:
		if action == 'remove':
			orderItem.quantity -= 1

	elif product.remaining_unit > orderItem.quantity:
		if action == 'add':
			orderItem.quantity += 1
		
		elif action == 'remove':
			orderItem.quantity -= 1

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	


	return JsonResponse('Item was added', safe=False)
