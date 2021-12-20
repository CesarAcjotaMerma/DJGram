from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

# Form
from posts.forms import PostForm

# Models
from posts.models import Post

class PostsFeedView(LoginRequiredMixin, ListView):
	template_name = 'posts/feed.html'
	model = Post
	ordering = { '-created',}
	paginate_by = 30
	context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):
	"""Create a new post"""
	template_name = 'posts/new.html'
	form_class = PostForm
	success_url = reverse_lazy('posts:feed')

	def get_context_data(self, **kwargs):
		"""Add user and profile to context."""
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
		context['profile'] = self.request.user.profile
		return context

@login_required
def list_posts(request):
   posts = Post.objects.all().order_by('-created')
   return render(request, 'posts/feed.html', {'posts': posts})
