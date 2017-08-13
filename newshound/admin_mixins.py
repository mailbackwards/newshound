from functools import update_wrapper
from collections import OrderedDict
import random

from django.conf.urls import url
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Dog
from .serializers import DogSerializer


### Dynamic action mixin

def make_field_action(field_name, field_verbose_name, value, value_verbose_name):
    name = 'set_{}_to_{}'.format(field_name, value)
    description = 'Set {} to "{}"'.format(field_verbose_name, value_verbose_name)

    def action(modeladmin, request, queryset):
        qs_count = queryset.update(**{field_name: value})
        messages.success(request,
            '{} item(s) successfully set to "{}"'.format(qs_count, value_verbose_name)
        )
    return action, name, description


class ActionFieldMixin(object):
    """
    Specify any `action_fields` (a BooleanField or CharField with choices).
    Adds an action to the list view for each choice.
    """
    action_fields = []

    def get_actions(self, request):
        # if it's explicitly set to None, don't show any
        if self.actions is None:
            return OrderedDict()
        actions = super(ActionFieldMixin, self).get_actions(request)

        permission = '{m.app_label}.change_{m.model_name}'.format(m=self.model._meta)
        if not request.user.has_perm(permission):
            return actions

        action_fields = [self.model._meta.get_field(field)
                         for field in self.action_fields]
        for field in action_fields:
            # should probably do better field validation here...
            choices = field.choices or [(True, 'True'), (False, 'False')]
            for value, verbose_name in choices:
                action = make_field_action(
                    field.name, field.verbose_name, value, verbose_name)
                actions[action[1]] = action
        return actions


### Custom view mixin

def get_trending_dogs(obj):
    """Advanced machine learning dog trend detection algorithm goes here..."""
    dogs = Dog.objects.all()
    return random.sample(list(dogs), 3)


class TrendingDogMixin(object):
    def trending(self, request, object_id, **kwargs):
        if request.method == 'GET':
            obj = get_object_or_404(self.model, id=object_id)
            # Advanced machine learning dog trend detection algorithm here...
            trending_dogs = get_trending_dogs(obj)
            dogs = DogSerializer(trending_dogs, many=True).data
            return JsonResponse({'dogs': dogs, 'success': True})
        else:
            return JsonResponse({'dogs': None, 'success': False})

    def get_urls(self):
        urls = super(TrendingDogMixin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        suggest_urls = [
            url(r'^(.+)/change/trending/$', wrap(self.trending),
                name='%s_%s_trending' % info)
        ]
        return suggest_urls + urls

    class Media:
        js = (('dog_trending.js'),)
