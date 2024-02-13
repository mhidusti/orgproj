from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from ..forms import CustomUserCreation




class SignUpView(CreateView):
     template_name = 'registration/signup.html'
     form_class = CustomUserCreation
     success_url = '/accounts/login/' #'registration/login' 

     def form_valid(self, form):
        form.save()
        email = self.request.POST.get('email')
        password = self.request.POST.get('password1')   
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request,user)
            return redirect('/accounts/edit-profile/%i'%(user.id-1))
        
     def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Invalid email or password')
        return super().form_invalid(form)