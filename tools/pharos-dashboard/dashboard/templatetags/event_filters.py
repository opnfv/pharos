from django.template.defaultfilters import register


@register.filter
def action_icon(value):
    if value == 'delete':
        return 'fa-remove'
    if value == 'change':
        return 'fa-edit'
    if value == 'create':
        return 'fa-star'
    return ''
