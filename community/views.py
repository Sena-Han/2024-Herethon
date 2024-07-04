from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import PostForm, CommentForm
from .models import Post, Category, Comment

def post(request):
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    search_type = request.GET.get('search_type')
    posts = Post.objects.all()

    if category_filter:
        posts = posts.filter(category__name=category_filter)

    if search_query:
        if search_type == 'title':
            posts = posts.filter(title__icontains=search_query)
        elif search_type == 'content':
            posts = posts.filter(content__icontains=search_query)
        elif search_type == 'nickname':
            posts = posts.filter(author__nickname__icontains=search_query)

    return render(request, 'post.html', {'posts': posts, 'categories': categories})


def post_category(request, category_name):
    categories = Category.objects.all()
    category_filter = category_name
    search_query = request.GET.get('search')
    search_type = request.GET.get('search_type')
    posts = Post.objects.all()

    if category_filter:
        posts = posts.filter(category__name=category_filter)

    if search_query:
        if search_type == 'title':
            posts = posts.filter(title__icontains=search_query)
        elif search_type == 'content':
            posts = posts.filter(content__icontains=search_query)
        elif search_type == 'nickname':
            posts = posts.filter(author__nickname__icontains=search_query)

    return render(request, 'post.html', {'posts': posts, 'categories': categories, 'selected_category': category_filter})

def postwrite(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post')
    else:
        form = PostForm()

    return render(request, 'postwrite.html', {'form': form})

def postdelete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect('post')

def postedit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect('postdetail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'postedit.html', {'form': form, 'post': post})

def postdetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, parent=None)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = request.POST.get('parent')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    return render(request, 'postdetail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_pk = comment.post.pk

    if comment.replies.exists():
        # 답글이 있는 경우 댓글 내용을 변경
        comment.content = "삭제된 댓글입니다."
        comment.is_deleted = True
        comment.save()
    else:
        # 답글이 없는 경우 댓글 삭제
        comment.delete()

    return redirect('postdetail', pk=post_pk)