from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from twilio.rest import Client
from .forms import SignUpForm, EmailVerificationForm, VerifyCodeForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.conf import settings


JOB_CATEGORIES = [
    '경영/관리', 'IT/인터넷', '연구개발/설계', '마케팅/PR', '전문직', '디자인', '방송/언론', '교육 전문직', '의료전문직', '영업', '건설', '생산/제조', '금융전문직', '생활/서비스', '문화/예술', '조사/분석',
    '공무원/정치인', '기타전문직'
]

def email_verification_view(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = get_random_string(length=6, allowed_chars='1234567890')
            request.session['verification_code'] = code
            request.session['verification_email'] = email
            send_mail(
                '인증 코드',
                f'인증 코드는 {code} 입니다.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return redirect('verify_code')
    else:
        form = EmailVerificationForm()
    return render(request, 'accounts/email_verification.html', {'form': form})

def verify_code_view(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('verification_code'):
                request.session['is_email_verified'] = True
                return redirect('signup')
            else:
                messages.error(request, 'Invalid verification code.')
    else:
        form = VerifyCodeForm()
    return render(request, 'accounts/verify_code.html', {'form': form})

def resend_code_view(request):
    email = request.session.get('verification_email')
    if email:
        code = get_random_string(length=6, allowed_chars='1234567890')
        request.session['verification_code'] = code
        send_mail(
            'Verification Code',
            f'Your new verification code is {code}.',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Verification code has been resent to your email.')
    return redirect('verify_code')

def signup_view(request):
    if not request.session.get('is_email_verified'):
        return redirect('email_verification')

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = True
            user.save()
            form.save()
            login(request, user)
            return redirect('job_selection')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def job_selection_view(request):
    if request.method == 'POST':
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        job_category = request.POST.get('job_category')
        if job_category and start_year and end_year:
            user = request.user
            user.start_year = start_year
            user.end_year = end_year
            user.job_category = job_category
            user.save()
            return redirect('welcome')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'accounts/job_selection.html', {'job_categories': JOB_CATEGORIES})

def welcome_view(request):
    return render(request, 'accounts/welcome.html')

def index_view(request):
    return render(request, 'accounts/index.html')

class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'



