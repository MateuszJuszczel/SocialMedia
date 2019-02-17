from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})


def dead_end(request):
    return render(request, 'main/dead_end.html')


class PostListView(ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    fields = ['title', 'content']
    template_name = 'main/detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'main/form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserPassesTestMixin():
    def get_test_func(self):
        pass


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'main/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def check_if_user(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'main/delete.html'
    success_url = '/'

    def check_if_user(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
