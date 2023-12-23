from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record

from .forms import SignUpForm, AddRecordForm

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successful login')
            return redirect('home')
        else:
            messages.success(request, 'Server error')
        
    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, 'Successful logout')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Successful registration')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'Authentication is required')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_item = Record.objects.get(id=pk)
        delete_item.delete()
        messages.success(request, 'Record deleted')
        return redirect('home')
    else:
        messages.success(request, 'Authentication is required')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'Authentication is required')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                add_record = form.save()
                messages.success(request, 'Record added')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    messages.success(request, 'Authentication is required')
    return redirect('home')