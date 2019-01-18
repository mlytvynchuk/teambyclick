from django import template
register = template.Library()

@register.simple_tag(name="get_companion")
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None