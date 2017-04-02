from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, PostViewer
from .forms import PostForm, CommentForm, ViewerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def post_list(request):
	post_pairs = PostViewer.objects.filter(viewer=request.user)
	posts = []
	for post_pair in post_pairs:
		posts.append(post_pair.post)
	#posts = posts.objects.order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
	    form = CommentForm(request.POST)
	    if form.is_valid():
	        comment = form.save(commit=False)
	        comment.created_date = timezone.now()
	        comment.post = post
	        comment.save()
	        return redirect('post_detail', pk=comment.post.pk)
	else:
	    form = CommentForm()
	return render(request, 'blog/post_detail.html', {'post': post, 'form': form})
	#return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		form2 = ViewerForm(request.POST)
		if (form.is_valid() & form2.is_valid()):
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			viewer = form2.save(commit=False)
			viewer.post = post
			viewer.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
		form2 = ViewerForm(request.POST)
	return render(request, 'blog/post_edit.html', {'form': form, 'form2': form2})

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


'''def comment_new(request):
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			post.created_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=comment.post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/post_detail.html', {'form': form})'''
