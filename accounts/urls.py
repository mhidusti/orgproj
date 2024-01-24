from django.urls import path, include
from .views import *


app_name = 'accounts'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit-profile/<int:pk>', EditProfileView.as_view(), name='profile'),
    path('api/V1/', include('accounts.api.V1.urls'))
]
