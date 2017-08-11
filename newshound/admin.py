from collections import OrderedDict
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Post, Dog, Breed, BreedGroup, DogBreedRelationship


# NOTE: this could be abstracted one more level to a `ChoiceActionMixin`.
# Put a `choice_actions` attr on the admin and use it to dynamically make

def make_pub_status_action(value, verbose_name):
    """Makes an admin action that updates publication_status to `value`."""
    action_name = 'set_pub_status_to_%s' % verbose_name.lower()
    description = 'Set publication status to "%s"' % verbose_name

    def action(modeladmin, request, queryset):
        qs_count = queryset.update(publication_status=value)
        msg_intro = 'One item was' if qs_count == 1 else '%d items were' % qs_count
        msg = '%s successfully set to "%s"' % (msg_intro, verbose_name)
        messages.success(request, msg)
    return action, action_name, description


class PubStatusActionMixin(object):
    """
    Mixin for the content admin that replaces the bulk-delete action with
    bulk-set actions for each of the `publication_status` choices.
    These are limited to editors and superusers.
    """
    def get_actions(self, request):
        # if it's explicitly set to None, don't show any
        if self.actions is None:
            return OrderedDict()

        actions = super(PubStatusActionMixin, self).get_actions(request)
        if request.user.is_superuser:
            for value, verbose_name in Post.PUB_STATUS_CHOICES:
                action = make_pub_status_action(value, verbose_name)
                actions[action[1]] = action
        return actions


class DogBreedInline(admin.TabularInline):
    model = DogBreedRelationship


class DogInline(admin.TabularInline):
    model = Post.dogs_mentioned.through


class PostAdmin(PubStatusActionMixin, admin.ModelAdmin):
    model = Post
    inlines = [DogInline]
    list_display = ['__str__', 'headline', 'dogs', 'publication_status', 'pub_date']
    list_editable = ['headline']

    def dogs(self, obj):
        """
        dogs_mentioned is a ManyToManyField, so this `dogs` list_display method
        lets it show up.

        format_html with hyperlinks to
        """
        return format_html('<br />'.join([
            '{0} <a href="{1}" target="_blank" alt="Link to {0}\'s detail page">&#x2197;</a>'.format(dog.name, dog.get_absolute_url())
            for dog in obj.dogs_mentioned.all()
        ]))

    def breeds(self, obj):
        pass

    def breed_groups(self, obj):
        pass


class DogAdmin(admin.ModelAdmin):
    model = Dog
    inlines = [DogBreedInline]


class BreedAdmin(admin.ModelAdmin):
    model = Breed


class BreedGroupAdmin(admin.ModelAdmin):
    model = BreedGroup


admin.site.register(Post, PostAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(BreedGroup, BreedGroupAdmin)
