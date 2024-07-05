from datetime import date

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, EmailVerificationForm, VerifyCodeForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required


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
    return render(request, 'email_verification.html', {'form': form})

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
    return render(request, 'verify_code.html', {'form': form})

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
        # Get date of birth fields
        year = request.POST.get('date_of_birth_year')
        month = request.POST.get('date_of_birth_month')
        day = request.POST.get('date_of_birth_day')

        # Validate and create date_of_birth
        try:
            date_of_birth = date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            date_of_birth = None
            messages.error(request, 'Invalid date of birth.')

        if form.is_valid() and date_of_birth:
            user = form.save(commit=False)
            user.date_of_birth = date_of_birth
            user.email_verified = True
            user.save()
            return redirect('job_selection')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def job_selection_view(request):
    if request.method == 'POST':
        job_category = request.POST.get('job_category')
        if job_category:
            user = request.user
            user.job_category = job_category
            user.save()
            return redirect('index')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'job_selection.html', {'job_categories': JOB_CATEGORIES})

def welcome_view(request):
    return render(request, 'welcome.html')

def index_view(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth_login(request, user)
                return redirect('home:home')
    else:
        form = AuthenticationForm() 
    return render(request, 'login.html', {'form': form})
