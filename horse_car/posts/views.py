from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from .models import Post, Order
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

# Create your views here.
# @login_required
# def add_post(request):
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST)
#         if post_form.is_valid():
#             # post_form.cleaned_data['users'] = request.user
#             post_form.instance.users = request.user
#             post_form.save()
#             return redirect('homepage')
#     else:
#         post_form = forms.PostForm(request.POST)
#     return render(request, 'add_post.html', {'form' : post_form})


# add post using class based view

@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('add_post')
    def form_valid(self, form):
        form.instance.users = self.request.user
        return super().form_valid(form)


# @login_required
# def edit_post(request, id):
#     post = models.Post.objects.get(pk=id)
#     post_form = forms.PostForm(instance=post)
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST, instance=post)
#         if post_form.is_valid():
#             post_form.instance.users = request.user
#             post_form.save()
#             return redirect('homepage')    
#     return render(request, 'add_post.html', {'form' : post_form})


# update post using class based view
@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')



# @login_required
# def delete_post(request, id):
#     post = models.Post.objects.get(pk=id)
#     post.delete()
#     return redirect('homepage')


# delete post using class based view
@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post   
    template_name = 'delete.html'   
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'


@login_required
def is_complete(request, id):
    post = models.Post.objects.get(pk=id)
    post.is_completed = True
    post.save()
    return redirect('homepage')





@login_required
def buy_now(request, id):
    post = Post.objects.get(pk=id)
    if post.quantity > 0:        
        post.quantity -= 1
        post.save()
        order = Order(user=request.user, post=post)
        order.save()
        messages.success(request, 'Buy Successfully')
        return redirect('profile')
    else:
        messages.warning(request, 'Out of Stock')
        return redirect('profile')





class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been added.')
        else:
            messages.error(request, 'There was an error with your comment.')
        return redirect('detail_post', id=post.id)         

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()      
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context




