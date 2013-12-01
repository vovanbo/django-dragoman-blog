from django import template
from dragoman_blog.models import EntryTranslation, TranslationTagged
from django.utils.translation import get_language
from django.db.models import Count
from datetime import datetime

register = template.Library()


@register.inclusion_tag('admin/dragoman_blog/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {
        'opts': opts,
        'onclick_attrib': (opts.get_ordered_objects() and change
                           and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                             and change and context.get('show_delete', True)),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    if context.get('translation_language_code') is not None:
        ctx['translation_language_code'] = context['translation_language_code']
    if context.get('translation_language_field') is not None:
        ctx['translation_language_field'] = context['translation_language_field']
    return ctx


# Tags below are inspired by Mezzanine
# https://github.com/stephenmcd/mezzanine/blob/master/mezzanine/blog/templatetags/blog_tags.py

@register.assignment_tag
def blog_months(*args):
    dates = EntryTranslation.objects.filter(
        is_published=True, language_code=get_language()).values_list("pub_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.assignment_tag
def blog_tags(*args):
    posts = EntryTranslation.objects.filter(
        is_published=True, language_code=get_language())
    tags = TranslationTagged.objects.none()
    for post in posts:
        tags = tags | TranslationTagged.tags_for(EntryTranslation, post)
    return list(tags.annotate(post_count=Count('dragoman_blog_translationtagged_items')).order_by('-post_count', 'name'))
