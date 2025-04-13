from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User

class LoginForm(forms.Form):
    """用户登录表单"""
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )

class UserCreationForm(BaseUserCreationForm):
    """创建用户表单"""
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'user_type', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入电话号码'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '请输入密码'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '请再次输入密码'})

class UserUpdateForm(forms.ModelForm):
    """更新用户表单"""
    class Meta:
        model = User
        fields = ('email', 'username', 'user_type', 'phone', 'is_active')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        exclude_type = kwargs.pop('exclude_type', False)
        super().__init__(*args, **kwargs)
        if exclude_type:
            self.fields.pop('user_type')
            self.fields.pop('is_active') 