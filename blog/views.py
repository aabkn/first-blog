from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

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

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

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
