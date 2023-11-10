from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings

from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (ListView, DetailView, UpdateView, CreateView, DeleteView, View)

from django_filters.views import FilterView

from .models import Post, Comment, User
from .forms import PostForm, CommentForm
from .filters import PostFilter
from .tasks import notify_about_new_post


class Posts(ListView):
    model = Post
    ordering = '-date_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount_posts'] = None

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    queryset = Post.objects.all()


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            post.author_post, created = User.objects.get_or_create(id=self.request.user.id)
            post.save()
            notify_about_new_post(pk=post.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()

        return context


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.author_post == self.request.user:
            self.template_name = 'post_delete.html'
            return self.template_name
        else:
            raise PermissionDenied


class Profile(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'profile.html'


class Search(FilterView):
    model = Post
    ordering = '-date_post'
    template_name = 'search.html'
    context_object_name = 'search'
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context


class Comments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    ordering = '-date_comment'
    paginate_by = 5

    def get_queryset(self):
        queryset = Comment.objects.filter(post_comment__author_post=self.request.user)
        return queryset


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'
    success_url = reverse_lazy('comments')

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author_comment = User.objects.get(id=self.request.user.id)
        comment.post_comment = Post.objects.get(id=self.kwargs['pk'])
        comment.save()
        result = super().form_valid(form)

        send_mail(
            subject=f'У Вашего объявления "{comment.post_comment.headline}" появился новый комментарий',
            message=f'Комментарий от {comment.author_comment}: "{comment.text_comment}"',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL]
        )
        return result


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'comment.html'
    queryset = Comment.objects.all()
    context_object_name = 'comment'

    def get_template_names(self):
        response = self.get_object()
        if response.post_comment.author_post == self.request.user:
            self.template_name = 'comment.html'
            return self.template_name
        else:
            raise PermissionDenied


@login_required
def confirm_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.confirmation_comment = True
    comment.save()
    send_mail(
        subject=f'Принят комментарий от {comment.author_comment}',
        message=f'Принят комментарий от {comment.author_comment} к объявлению {comment.post_comment.headline}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL]
    )
    return render(request, 'confirmation.html')


@login_required
def reject_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.confirmation_comment = False
    comment.save()
    return render(request, 'comments')




