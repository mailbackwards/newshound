from django.contrib.admin import AdminSite

from .models import Post, Dog, Breed, BreedGroup
from .admin import PostAdmin, DogAdmin, BreedAdmin, BreedGroupAdmin


class NewshoundAdmin(AdminSite):
    site_header = 'Newshound!'
    index_title = 'The dashboard for Newshound'
    login_template = 'custom_login.html'


admin_site = NewshoundAdmin(name='newshoundadmin')

admin_site.register(Post, PostAdmin)
admin_site.register(Dog, DogAdmin)
admin_site.register(Breed, BreedAdmin)
admin_site.register(BreedGroup, BreedGroupAdmin)
