# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
def login_view(request):
	print("is user authenticated ? : " + str(request.user.is_authenticated()))
	next = request.GET.get('next')
	title = "Connexion"
	form = UserLoginForm(request.POST or None)

	if request.user.is_authenticated():
		return redirect("/online-users")
	elif form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		login(request, user)
		if next:
		  	return redirect(next)
		return redirect("/online-users")
		print("Test authentication, is User logged ? : " + request.user.is_authenticated())
		# redirect
	return render(request, "registration/login.html", {"form": form, "title": title})

def register_view(request):
	print("is user authenticated ? : " + str(request.user.is_authenticated()))
	#next = request.GET.get('next')
	title = "Inscription"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(request, username=user.username, password=password)
		login(request, new_user)
		# if next
		# 	return redirect(next)
		return redirect("/online-users")

	context = {"form": form, "title": title}

	return render(request, "registration/registration.html", context)

def logout_view(request):
	logout(request)
	return redirect("/login")