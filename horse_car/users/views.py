from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post, Order
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.

# def add_user(request):
#     if request.method == 'POST':
#         user_form = forms.UserForm(request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             return redirect('add_user')
#     else:
#         user_form = forms.UserForm(request.POST)
#     return render(request, 'add_user.html', {'form' : user_form})

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():            
            messages.success(request, 'Account Created Successfully')
            register_form.save()
            return redirect('register')
    else:
        register_form = forms.RegistrationForm(request.POST)
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             user_name = form.cleaned_data['username']
#             user_pass = form.cleaned_data['password']
#             user = authenticate(username=user_name, password=user_pass)
#             if user is not None:
#                 messages.success(request, 'Logged in Successfully')
#                 login(request, user)
#                 return redirect('profile')
#             else:
#                 messages.warning(request, 'Login information incorrect')
#                 return redirect('register')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'register.html', {'form': form, 'type' : 'Login'})


# user login view class based view

class UserLoginView(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in Information Incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'login'
        return context




@login_required
def profile(request):    
    orders = Order.objects.filter(user=request.user)  
    return render(request, 'profile.html', {'orders': orders})       
    


@login_required
def edit_profile(request):
    if request.method == 'POST':
       profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
       if profile_form.is_valid():            
            messages.success(request, 'Profile Updated Successfully')
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'update_profile.html', {'form' : profile_form})



def pass_change(request):
    if request.method == 'POST':
        pass_change_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_change_form.is_valid():            
            messages.success(request, 'Password Updated Successfully')
            pass_change_form.save()
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('profile')
    else:
        pass_change_form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : pass_change_form})



def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('user_login')



# user logout view class based view

# class UserLoginView(LogoutView):
#     template_name = 'register.html'
#     # success_url = reverse_lazy('user_login')

#     def get_success_url(self):
#         return reverse_lazy('user_login')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['type'] = 'logout'
#         return context

