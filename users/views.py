"""User views."""

#Django Imports

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile

# Forms
from users.forms import SignupForm

class UserDetailView(LoginRequiredMixin, DetailView):
    """User Detail View"""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class SignUpView(FormView):
    """Users signup view"""

    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        form.save()

        username = form['username'].value()
        password = form['password'].value()

        user = authenticate(
            self.request, username=username, password=password)
        
        login(self.request, user)

        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})

class LoginView(auth_views.LoginView):
    """Login View"""

    template_name = 'users/login.html'

class LogoutView(auth_views.LogoutView):
    """Logout View"""

    template_name = 'users/logged_out.html'