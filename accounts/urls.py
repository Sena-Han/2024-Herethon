from django.urls import path
from .views import signup_view, email_verification_view, verify_code_view, LoginView, resend_code_view, job_selection_view, welcome_view
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('email-verification/', email_verification_view, name='email_verification'),
    path('verify-code/', verify_code_view, name='verify_code'),
    path('resend-code/', resend_code_view, name='resend_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('job-selection/', job_selection_view, name='job_selection'),
    path('welcome/', welcome_view, name='welcome'),
]
