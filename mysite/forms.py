from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	"""
	登录表单
	"""
	username = forms.CharField(
		label="用户名",
		required=True,
		widget=forms.TextInput(
			attrs={
				"class":"form-control",
				"placeholder":"输入用户名"
			}
		),
	)
	password = forms.CharField(
		label="密码",
		widget=forms.PasswordInput(
			attrs={
				"class":"form-control",
				"placeholder":"输入用密码"
			}
		),
	)
	
	def clean(self):
		username = self.cleaned_data["username"]
		password = self.cleaned_data["password"]

		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("用户名或密码错误")
		else:
			self.cleaned_data["user"] = user

		return self.cleaned_data


class RegisterForm(forms.Form):
	"""
	注册表单
	"""
	username = forms.CharField(
		label="用户名",
		max_length=30,
		min_length=3,
		widget=forms.TextInput(
			attrs={
				"class":"form-control",
				"placeholder":"输入用户名"
			}
		),
	)
	password = forms.CharField(
		label="密码",
		min_length=6,
		widget=forms.PasswordInput(
			attrs={
				"class":"form-control",
				"placeholder":"输入用密码"
			}
		),
	)
	password_again = forms.CharField(
		label="密码",
		min_length=6,
		widget=forms.PasswordInput(
			attrs={
				"class":"form-control",
				"placeholder":"再次输入用密码"
			}
		),
	)
	email = forms.EmailField(
		label="邮箱",
		widget=forms.EmailInput(
			attrs={
				"class":"form-control",
				"placeholder":"输入用邮箱"
			}
		),
	)


	def clean_username(self):
		username = self.cleaned_data["username"]
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("用户名已存在")
		return username


	def clean_email(self):
		email = self.cleaned_data["email"]
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("邮箱已存在")

		return email
		

	def clean_password_again(self):
		password = self.cleaned_data["password"]
		password_again = self.cleaned_data["password_again"]

		if password_again != password:
			raise forms.ValidationError("两次密码不一致")

		return password_again









