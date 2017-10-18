#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)



User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		#user_qs = User.objects.filter(username=username)
		# if user_qs.count() == 1:
		# 	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Cet utilisateur n'existe pas.")
			if not user.check_password(password):
				raise forms.ValidationError("Mot de passe incorrect")
			if not user.is_active:
				raise forms.ValidationError("Cet utilisateur n'est plus actif.")
		#Return default form.
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	email2 = forms.EmailField(label='Adresse e-mail.')
	email2 = forms.EmailField(label='Confirmez votre adresse e-mail.')
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'email2', 'password']

	def clean_email(self):
		print(self.cleaned_data)
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		print(email, email2)
		if email != email2:
			raise forms.ValidationError("Les e-mails doivent être identiques.")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Cet adresse e-mail est déjà enregistrée.")
		return email