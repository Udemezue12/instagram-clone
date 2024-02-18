# from allauth.account.forms import AllAuthPasswordResetForm
from allauth.account.views import PasswordSetView, PasswordChangeView
from django.contrib.auth.views import PasswordResetView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

from . import forms, models





def homepage(request):
    
    return render(request, 'content/base.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('content:home')
    else:
        form = AuthenticationForm()
    return render(request, 'content/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('content:home')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('content:home')
    else:
        form = UserCreationForm()
    return render(request, 'content/register.html', {'form': form})


def home(request):
    posts = models.Post.objects.order_by('created_at')

    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('content:home')  

    else:
        form = forms.PostForm()

    return render(request, 'content/home.html', {'posts': posts, 'form': form})



def post_create(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect('home')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            posta = form.save(commit=False)
            posta.user = request.user
            posta.save()
            return redirect('content:home')
    else:
        form = forms.PostForm()
    return render(request, 'content/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    context = {'post': post}
    return render(request, 'content/post_detail.html', context)


@login_required
def like_post(request, post_id):
    post = models.Post.objects.get(pk=post_id)
    (like, created) = models.Like.objects.get_or_create(
        user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = models.Post.objects.get(pk=post_id)
    if request.method == 'POST':
        comment = forms.CommentForm(request.POST)
        if comment.is_valid():
            add = comment.save(commit=False)
            add.user = request.user
            add.post = post
            return redirect('home')
    else:
        commit = forms.CommentForm()
    return render(request, 'content/add_comment.html', {'commit': commit})


@login_required
def delete_comment(request, comment_id):
    post = get_object_or_404(models.Comment, pk=comment_id)
    if request.user == post.user:
        post.delete()
        return redirect('home')
    else:
        return render(request, 'content/permission_denied.html', {'message': 'You do not have permission to delete this comment.'})


# def password_reset(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)

#             reset_url = reverse("password_reset_confirm", args=(uid, token))
#             send_mail(
#                 'Password Reset',
#                 f'Click the following link to reset your password: {reset_url}',
#                 'from@example.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#             messages.success(
#                 request, 'Password reset email sent. Check your inbox for further instructions.')
#             return redirect('home')

#     else:
#         form = PasswordResetForm()

#     return render(request, 'content/password_reset.html', {'form': form})

# def password_reset(request):
#     if request.method == 'POST':
#         form = AllAuthPasswordResetForm(request.POST)
#         if form.is_valid():
#             return AllAuthPasswordResetView.as_view()(request)
#     else:
#         form = AllAuthPasswordResetForm()

#     return render(request, 'content/password_reset.html', {'form': form})


# def password_reset(request):
#     return PasswordSetView.as_view(template_name='content/custom_password_reset.html')(request)
# def password_reset(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             # Generate a password reset token
#             user = form.get_user()
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)

#             # Construct the password reset link
#             reset_url = request.build_absolute_uri(
#                 f'/password-reset/confirm/{uid}/{token}/'
#             )

#             # Send a password reset email (customize this based on your email sending setup)
#             send_mail(
#                 'Password Reset',
#                 f'Click the following link to reset your password: {reset_url}',
#                 'from@example.com',
#                 [user.email],
#                 fail_silently=False,
#             )

#             messages.success(request, 'Password reset email sent. Check your inbox for further instructions.')
#             return redirect('content:home')  # Customize the redirect URL after sending the email
#     else:
#         form = PasswordResetForm()
#     return render(request, 'content/password_reset.html', {'form': form})
    

class PasswordResetView(PasswordResetView):
    template_name = 'content/password_reset.html'
    email_template_name = 'content/password_reset_email.html'
    success_url = reverse_lazy('content:password_reset_done')

    def get_success_url(self):
        
        return reverse_lazy('content:home')
    


def password_reset_confirm(request, uidb64, token):
    return PasswordSetView.as_view()(request, uidb64=uidb64, token=token)


def password_reset_complete(request):

    custom_data = {
        'message': 'Your password has been successfully reset.',
        'additional_info': 'You can now log in with your new password.',

    }

    return render(request, 'content/password_reset_complete.html', context=custom_data)


def password_reset_done(request):
    return PasswordChangeView.as_view()(request)
