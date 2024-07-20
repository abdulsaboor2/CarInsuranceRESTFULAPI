from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Account, Transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import random
from decimal import Decimal

def index(request):
    account = False
    if request.user.is_authenticated:
       if Account.objects.filter(user = request.user).exists():
           account = True
    print("account status: ", account)
    return render(request, 'index.html', {'account':account})

def DoTransection(sender, reciever, amount, status):
    Transaction.objects.create(
            sender = sender,
            receiver=reciever,
            amount=amount,
            status= status
        )
    return True

@login_required(login_url='login')
def transection(request):
    if request.method == "POST":
        user = request.user
        password = request.POST.get('password')
        try:
            sender_account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            messages.error(reqeust, "Internal Server Error Sender Account does not exist")
            return HttpResponseRedirect(request.path_info)
        
        user = authenticate(username=user.username, password=password)
        if user is None:
            messages.success(request, "Invalid Password")
            return HttpResponseRedirect(request.path_info)
       
        
        amount = Decimal(request.session.get('amount'))
        account_number = request.session.get('account_number')
        
        receiver_account = Account.objects.get(account_number=account_number)
        
        DoTransection(sender_account, receiver_account, amount, "send")
        sender_account.balance -= amount
        sender_account.save()
        
        DoTransection(sender_account, receiver_account, amount, "receive")
        receiver_account.balance += amount
        receiver_account.save()
        
        messages.success(request, "Transection has been done successfully!")
        return redirect('dashboard', username=user.username)
        
    return render(request, 'dashboard/money_transfer.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return HttpResponseRedirect(request.path_info)

        if not name or not username or not email or not password:
            messages.error(request, "All the fields are required")
            return HttpResponseRedirect(request.path_info)
            
        
        user = User(first_name=name, username=username, email=email, password=make_password(password))
        user.save()
        login(request, user)
        return redirect('login')

    return render(request, 'dashboard/pages/sign-up.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "All the fields are required")
            return HttpResponseRedirect(request.path_info)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return HttpResponseRedirect(request.path_info)

    return render(request, 'dashboard/pages/sign-in.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def dashboard(request, username):
    if request.user.username != username:
        return HttpResponse("You don't have permissions to access this page!")
    if not Account.objects.filter(user=request.user).exists():
        return redirect('home')
    
    user = User.objects.get(username=username)
    account = Account.objects.filter(user=user).first()
    Transections_send = Transaction.objects.filter(sender = account, status='send')
    Transections_receive = Transaction.objects.filter(receiver = account, status='receive')
    withdrawals = Transaction.objects.filter(sender=account, status='withdraw')
    recieve_count = Transaction.objects.filter(receiver = account, status='receive').count()
    send_count =Transaction.objects.filter(sender = account, status="send").count()
    
    
    context = {
        "account":account,
        "Transections_send":Transections_send,
        "Transections_receive":Transections_receive,
        "recieve_count":recieve_count,
        "send_count":send_count,
        "withdrawals":withdrawals,
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='login')
def create_account(request):
    user = request.user
    if Account.objects.filter(user = user).exists():
        return redirect('dashboard', username=user.username)
    if request.method == "POST":
        password = request.POST.get('password1')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        postal_code = request.POST.get('postcode')
        city = request.POST.get('city')
        country = request.POST.get('country')
        address = request.POST.get('address')
        account_type = request.POST.get('type')
        amount = request.POST.get('amount')

        if not ( password and email and dob and name and phone and postal_code and city and country and address):
            messages.error(request, "All fields are required.")
            return HttpResponseRedirect(request.path_info)

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return HttpResponseRedirect(request.path_info)

        account = Account(
            user=user,
            dob=dob,
            name=name,
            email=email,
            phone=phone, 
            postel_code=postal_code,
            city=city,
            country=country,
            address=address,
            account_type=account_type,
            balance=amount,
            status=True  
        )
        account.save()
        
        user = request.user
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect('dashboard', username=user.username)  

    return render(request, 'accounts/create_account.html')  

@login_required(login_url="login")
def payment_invoice(request, id):
    user = request.user
    transection = Transaction.objects.get(transaction_id=id)
    account = Account.objects.get(user = user)
    
    context = {
        'transection': transection,
        'account': account,
    }
    return render(request, 'invoice.html', context)


@login_required(login_url='login')
def validate_and_fetch_account(request):
    if request.method == "POST":
        account_number = request.POST.get('receiver')
        amount = request.POST.get('amount')
        
        flag = False

        try:
            receiver_account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            messages.error(request, "Account dost not exit")
            return redirect('transections')

        account = Account.objects.get(user=request.user)
        if account.balance < float(amount):
            messages.error(request, "Insufficient balance")
            return redirect('transections')

        request.session['account_number'] = account_number
        request.session['amount'] = amount
        
        flag = True
        context = {
            'name': receiver_account.name,
            'flag':flag,
        }
        print(flag)
        return render(request, 'dashboard/money_transfer.html', context)

    return redirect('transections')


@login_required(login_url='login')
def withdraw_amount(request):
    if request.method == "POST":
        user = request.user
        account = Account.objects.get(user=user)
        amount = request.POST.get('amount')
        password = request.POST.get('password')
         
        user = authenticate(username=user.username, password=password)
        if user is None:
            messages.success(request, "Invalid Password")
            return HttpResponseRedirect(request.path_info)
        
        if account.balance < float(amount):
            messages.error(request, "Insufficient balance")
            return redirect('withdraw')
        
        DoTransection(account, account, amount, "withdraw")
        account.balance -= Decimal(amount)
        account.save()
        
        messages.success(request, "Amount has been widthrawl successfully!")
        return redirect('dashboard', username=user.username)
    return render(request, 'dashboard/withdraw.html')

