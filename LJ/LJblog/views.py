# Create your views here.
import sys
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import *
from forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect



@csrf_protect
def blog_search(request):
    if request.method == 'POST':
        key = request.POST['search_text'].encode('utf8')
        posts = Post.objects
        filter_blog = posts.filter(title__contains=key)
        print filter_blog
        return redirect( '/' )

class PostListView(ListView):
    model = Post
    context_object_name = "post_list"

    def get_template_names(self):
        return ["LJblog/list.html"]

    def get_queryset(self):
        posts = Post.objects
        if 'all_posts' not in self.request.GET:
            posts = posts.filter(is_published=True)
        return posts

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_template_names(self):
        return ["LJblog/create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
       if self.request.method == 'POST':
        form.tag = self.request.POST.getlist('mytext')

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        messages.success(self.request, "The post has been created.")
        return super(PostCreateView, self).form_valid(form)

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

    def get_template_names(self):
        return ["LJblog/detail.html"]

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    context_object_name = "post"

    def get_template_names(self):
        return ["LJblog/update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        if self.request.method == 'POST':
            form.tag = self.request.POST.getlist('mytext')

         
            self.object = form.save()
            messages.success(self.request, "The post has been updated.")
            return super(PostUpdateView, self).form_valid(form)

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]

class AddComment(UpdateView):
    model = Post
    form_class = CommentForm
    context_object_name = "post"

    def get_template_names(self):
        return ["LJblog/comment.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        if self.request.method == 'POST':
            # print "hello"
            form.name = self.request.POST.get('name')
            form.comment_text = self.request.POST.get('comment_text')
           
            # self.object = form.save()
            messages.success(self.request, "The Comment has been added.")
            return super(AddComment, self).form_valid(form)

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The post has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]


