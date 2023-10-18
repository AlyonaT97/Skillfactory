from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
    # LANGUAGE_SESSION_KEY

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView, View
)

from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm, BaseRegisterForm

import pytz


class PostList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'posts.html'
    context_object_name = _('posts')
    paginate_by = 10
    form_class = PostForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['categories'] = Category.objects.all()
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(LoginRequiredMixin, DetailView):
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
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'post_search.html'
    context_object_name = _('posts')
    paginate_by = 5
    form_class = PostForm

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_search')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.post_type = 'AR'
        print(self.request.path)
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('news_create')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.change_post'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('signup')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class CategoryList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = _('posts')
    paginate_by = 5
    form_class = PostForm

    def get_queryset(self):
        self.post_category = Category.objects.get(pk=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        context['is_not_subscriber'] = self.request.user not in category.subscribers.all()
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        context['category'] = category

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


@login_required
def became_author(request):
    user = request.user
    Author.objects.create(user=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    return redirect('/posts/')


class Index(View):
    def get(self, request):

        current_time = timezone.now()

        models = Post.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones
        }

        return HttpResponse(render(request, 'posts.html', context))





