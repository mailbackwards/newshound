from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import format_html

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset
from django_admin_row_actions import AdminRowActionsMixin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin

from .admin_mixins import ActionFieldMixin, TrendingDogMixin
from .models import Post, Dog, Breed, BreedGroup, DogBreedRelationship


class PostAdmin(DjangoObjectActions,
                AdminRowActionsMixin,
                InlineActionsModelAdminMixin,
                ActionFieldMixin,
                TrendingDogMixin,
                admin.ModelAdmin):
    model = Post
    list_display = ['pub_date', 'headline', 'publication_status']
    list_editable = ['headline']
    action_fields = ['publication_status']  # from ActionFieldMixin
    inline_actions = ['make_dogs_good', 'publish_edited'] # from InlineActions

    ### Admin defaults ###

    def get_queryset(self, request):
        # prefetch the fields we'll be using
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.prefetch_related('dogs_mentioned')

    ### Custom display methods ###

    def dogs(self, obj):
        # adds a 'dogs' column with a link to view details for each
        dog_html = [(
            '{name} <a href="{absurl}" target="_blank" '
            'alt="Link to {name}\'s detail page">&#x2197;</a>'.format(
                name=dog.name, absurl=dog.get_absolute_url())
        ) for dog in obj.dogs_mentioned.all()]
        return format_html('<br />'.join(dog_html))

    ### Row actions ###

    def get_row_actions(self, obj):
        row_actions = [{
            'label': 'Delete',
            'url': reverse('admin:newshound_post_delete', args=[obj.id]),
        }, {
            'label': 'Good dogs',
            'action': 'make_dogs_good',
            'tooltip': 'Turn all the dogs into good dogs',
        }]
        row_actions += super(PostAdmin, self).get_row_actions(obj)
        return row_actions

    ### Object actions ###

    def make_dogs_good(self, request, obj, parent_obj=None):
        """Set all dogs mentioned in this article to be `good`. Good dogs!"""
        num_dogs = obj.dogs_mentioned.update(is_good=True)
        self.message_user(request, '{} dogs are now good'.format(num_dogs))
    make_dogs_good.label = 'Make dogs good'
    make_dogs_good.short_description = 'Set all dogs in this post to be Good'

    @takes_instance_or_queryset
    def view_breeds(self, request, queryset):
        """Provide a shortcut link to breeds in both changelist and change views."""
        return redirect('admin:newshound_breed_changelist')
    view_breeds.label = 'View breeds'

    def publish_edited(modeladmin, request, queryset):
        """Publish all items currently marked as `Edit`. Includes a confirmation view."""
        edit_posts = queryset.filter(publication_status=Post.PUB_STATUS_EDIT)
        if 'confirm' in request.POST:
            num_posts = edit_posts.update(publication_status=Post.PUB_STATUS_PUBLISHED)
            messages.success(request, '{} post(s) updated'.format(num_posts))
            return None
        else:
            return render(request, 'publish_confirm.html', {'posts': edit_posts})
    publish_edited.label = 'Publish all edits'

    # Set the object_actions
    changelist_actions = ('view_breeds', 'publish_edited')
    change_actions = ('view_breeds', 'make_dogs_good')


class DogAdmin(ActionFieldMixin, admin.ModelAdmin):
    model = Dog
    action_fields = ['is_good']     # from ActionFieldMixin


class DogBreedInline(admin.TabularInline):
    model = DogBreedRelationship


class DogInline(admin.TabularInline):
    model = Post.dogs_mentioned.through


class BreedAdmin(admin.ModelAdmin):
    model = Breed


class BreedGroupAdmin(admin.ModelAdmin):
    model = BreedGroup


admin.site.register(Post, PostAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(BreedGroup, BreedGroupAdmin)
