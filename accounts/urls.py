from django.urls import path

from home.views import home
from .views import signup_view, email_verification_view, verify_code_view, login, resend_code_view, job_selection_view, welcome_view, mypage_view, mypage_post, post_list_view, comment_list_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('email-verification/', email_verification_view, name='email_verification'),
    path('verify-code/', verify_code_view, name='verify_code'),
    path('resend-code/', resend_code_view, name='resend_code'),
    path('login/', login, name='login'),
    path('job-selection/', job_selection_view, name='job_selection'),
    path('welcome/', welcome_view, name='welcome'),
    path('home/', home, name='home'),
    path('mypage/', mypage_view, name='mypage'),
    path('mypage/mypagepost', mypage_post, name='mypagepost'),
    path('mypage/posts/', post_list_view, name='my-posts'),
    path('mypage/comments/', comment_list_view, name='my-comments'),
]
