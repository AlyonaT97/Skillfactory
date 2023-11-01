from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.cache import cache

from django.views.generic import (ListView, DetailView, UpdateView, CreateView, DeleteView)

from .models import Post, Category, Comment
from .forms import PostForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-date_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    form_class = PostForm

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filteset'] = self.filterset
        context['form'] = self.form_class()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()
    form_class = PostForm

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostCreate(CreateView):
    model = Post
    template_name = 'createpost.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class PostEdit(UpdateView):
    model = Post
    template_name = 'editpost.html'
    success_url = reverse_lazy('post_detail')
