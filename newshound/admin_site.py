from django.contrib.admin import AdminSite

from .models import Post, Dog, Breed, BreedGroup
from .admin import PostAdmin, DogAdmin, BreedAdmin, BreedGroupAdmin


class NewshoundAdmin(AdminSite):
    """
    A custom AdminSite so we can customize the names and basic forms.
    """
    site_header = 'Newshound!'
    index_title = 'The dashboard for Newshound'
    login_template = 'custom_login.html'


admin_site = NewshoundAdmin(name='newshoundadmin')

# Register admin models here instead of using autodiscover
admin_site.register(Post, PostAdmin)
admin_site.register(Dog, DogAdmin)
admin_site.register(Breed, BreedAdmin)
admin_site.register(BreedGroup, BreedGroupAdmin)
