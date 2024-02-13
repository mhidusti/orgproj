from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from ..forms import AuthenticationForm






class LoginView(FormView):
     template_name = 'registration/login.html'
     form_class = AuthenticationForm
     success_url = '/'

     def form_valid(self, form):
         email = self.request.POST.get('email')
         password = self.request.POST.get('password')
         user = authenticate(email=email, password=password)
         if user is not None:
              login(self.request, user)
              return super().form_valid(form)