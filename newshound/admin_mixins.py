from collections import OrderedDict
from django.contrib import messages


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
