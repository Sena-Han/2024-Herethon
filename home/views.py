from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from community.models import Post
from .forms import AdviceForm
from .models import Advice


# 홈 세팅
def home(request):
    one_month_ago = timezone.now() - timedelta(days=30)

    top_qa_posts = Post.objects.filter(category__name='Q&A', created_at__gte=one_month_ago).order_by('-likes', '-created_at')[:3]
    top_lounge_posts = Post.objects.filter(category__name='라운지', created_at__gte=one_month_ago).order_by('-likes', '-created_at')[:3]
    top_ama_posts = Post.objects.filter(category__name='AMA', created_at__gte=one_month_ago).order_by('-likes', '-created_at')[:3]
    top_advices = Advice.objects.filter(created_at__gte=one_month_ago).order_by('-likes', '-created_at')[:3]

    context = {
        'top_qa_posts': top_qa_posts,
        'top_lounge_posts': top_lounge_posts,
        'top_ama_posts': top_ama_posts,
        'top_advices': top_advices,
    }

    return render(request, 'home.html', context)


# 조언 리스트
def advice_list(request):
    advices = Advice.objects.all().order_by('-created_at')
    return render(request, 'advice_list.html', {'advices': advices})


# 조언 상세
def advice_detail(request, advice_id):
    advice = get_object_or_404(Advice.objects.order_by('-created_at'), id=advice_id)
    return render(request, 'advice_detail.html', {'advice': advice})


# 조언 작성
@login_required
def advice_write(request):
    user = request.user
    job_type = user.job_type  # 사용자의 직업 정보 확인

    if not job_type:
        # job_type 정보가 없는 경우 에러 메시지 출력 후 리다이렉트
        messages.error(request, '직업 정보를 입력하기 전에는 작성할 수 없습니다.')
        return redirect('home:advice_list')

    if request.method == 'POST':
        form = AdviceForm(request.POST, request.FILES)
        if form.is_valid():
            advice = form.save(commit=False)
            advice.author = user
            advice.save()
            return redirect('home:advice_detail', advice_id=advice.id)
    else:
        form = AdviceForm()

    return render(request, 'advice_write.html', {'form': form})


# 조언 수정
@login_required
def advice_edit(request, advice_id):
    advice = get_object_or_404(Advice, id=advice_id)
    if request.user != advice.author and not request.user.is_staff:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('home:advice_detail', advice_id=advice_id)

    if request.method == 'POST':
        form = AdviceForm(request.POST, request.FILES, instance=advice)
        if form.is_valid():
            form.save()
            messages.success(request, '게시물이 수정되었습니다.')
            return redirect('home:advice_detail', advice_id=advice_id)
    else:
        form = AdviceForm(instance=advice)

    return render(request, 'advice_edit.html', {'form': form, 'advice': advice})


# 조언 삭제
@login_required
def advice_delete(request, advice_id):
    advice = get_object_or_404(Advice, id=advice_id)
    if request.user == advice.author or request.user.is_staff:
        advice.delete()
        messages.success(request, '게시물이 삭제되었습니다.')
        return redirect('home:advice_list')
    else:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('home:advice_detail', advice_id=advice_id)


# 조언 좋아요
@login_required
def advice_like(request, advice_id):
    advice = get_object_or_404(Advice, id=advice_id)
    if advice.author == request.user:
        messages.error(request, '작성자는 좋아요를 누를 수 없습니다.')
    else:
        if advice.likes.filter(id=request.user.id).exists():
            advice.likes.remove(request.user)
        else:
            advice.likes.add(request.user)
    return redirect('home:advice_detail', advice_id=advice_id)
