from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost
from analytics.models import View
from django.http import Http404


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'

    def get_object(self, queryset=None):
        post_pk = self.kwargs.get('pk')
        if post_pk:
            post_query = BlogPost.objects.filter(pk=post_pk)
            if post_query.exists():
                post_object = post_query.first()
                view, created = View.objects.get_or_create(
                    user=self.request.user,
                    post=post_object
                )
                if view:
                    view.views_count += 1
                    view.save()

                return post_object
        raise Http404


