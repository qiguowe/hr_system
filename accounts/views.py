from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import User
from .decorators import system_admin_required, admin_required
from .forms import LoginForm, UserCreationForm, UserUpdateForm

def login_view(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, '邮箱或密码不正确')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """用户注销视图"""
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """用户仪表盘视图"""
    context = {}
    return render(request, 'accounts/dashboard.html', context)

@system_admin_required
def user_list(request):
    """用户列表视图 - 仅系统管理员可访问"""
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@system_admin_required
def user_create(request):
    """创建用户视图 - 仅系统管理员可访问"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '用户创建成功')
            return redirect('user_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/user_form.html', {'form': form, 'title': '创建用户'})

@system_admin_required
def user_update(request, pk):
    """更新用户视图 - 仅系统管理员可访问"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '用户更新成功')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'accounts/user_form.html', {'form': form, 'title': f'编辑用户: {user.username}'})

@system_admin_required
def user_delete(request, pk):
    """删除用户视图 - 仅系统管理员可访问"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, '用户删除成功')
        return redirect('user_list')
    
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})

@login_required
def profile(request):
    """用户个人资料视图"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user, exclude_type=True)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user, exclude_type=True)
    
    return render(request, 'accounts/profile.html', {'form': form})
