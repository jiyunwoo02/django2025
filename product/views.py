from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import MainContent, Comment
from .forms import CommentForm

def index(request):
    content_list = MainContent.objects.order_by('-pub_date')
    context = {'content_list': content_list}
    return render(request, 'product/content_list.html', context)

def detail(request, content_id):
    content_list = get_object_or_404(MainContent, pk=content_id)
    context = { 'content_list': content_list}
    return render(request, 'product/content_detail.html', context)

def comment_create(request, content_id):
    content_list = get_object_or_404(MainContent, pk=content_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
        comment.content_list = content_list
        comment.author = request.user
        comment.save()
        return redirect('detail', content_id=content_list.id)
    else:
        form = CommentForm()

    context = {'content_list': content_list, 'form': form}
    return render(request, 'product/content_detail.html', context)

# 비로그인 상태에서 댓글 작성 -> 로그인 화면으로 이동
@login_required(login_url='accounts:login')
def comment_create(request, content_id):
    content_list = get_object_or_404(MainContent, pk=content_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

    if form.is_valid():
            comment = form.save(commit=False)
            comment.content_list = content_list
            comment.author = request.user
            comment.save()
            return redirect('detail', content_id=content_list.id)
    else:
        form = CommentForm()

    context = {'content_list': content_list, 'form': form}
    return render(request, 'product/content_detail.html', context)

@login_required(login_url='accounts:login')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        raise PermissionDenied

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('detail', content_id=comment.content_list.id)
    else:
        form = CommentForm(instance=comment)

    context = {'comment': comment, 'form': form}
    return render(request, 'product/comment_form.html', context)

@login_required(login_url='accounts:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        raise PermissionDenied
    else:
        comment.delete()
    return redirect('detail', content_id=comment.content_list.id)

# 상품 검색 기능
def product_list(request):
    query = request.GET.get('q', '')  # 검색어 가져오기 (기본값 '')
    if query:
        content_list = MainContent.objects.filter(title__icontains=query)  # 제목 검색
    else:
        content_list = MainContent.objects.all()  # 검색어 없으면 전체 목록

    return render(request, 'product/content_list.html', {'content_list': content_list, 'query': query})