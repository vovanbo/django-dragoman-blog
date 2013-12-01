from dragoman_blog.models import EntryTranslation, UniTag
from django.views.generic.list import ListView
from django.utils.translation import get_language


class ListByTagView(ListView):

    """ View for listing posts by tags"""
    template_name = "dragoman_blog/entrytranslation_list_by_tag.html"
    model = EntryTranslation

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        if (tag != ''):
            object_list = self.model.objects.filter(
                tags__slug=tag, language_code=get_language(), is_published=True)
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ListByTagView, self).get_context_data(**kwargs)
        tag = UniTag.objects.get(slug=self.kwargs.get('tag', ''))
        context['tag'] = tag
        return context
