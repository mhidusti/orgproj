from ..models import  Profile
from django.views.generic import UpdateView


class EditProfileView(UpdateView):
    template_name = 'registration/edit_profile.html'
    model = Profile
    fields = [ 'user','first_name', 'last_name', 'image', 'phone', 'address']
    success_url = '/'