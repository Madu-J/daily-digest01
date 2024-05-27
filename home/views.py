from django.views import generic, View
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Comment, UserProfile
from .forms import CommentForm, ProfileForm, PostForm


class Home(generic.TemplateView):
    """This view is used to display the home page"""
    template_name = "index.html"


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "browse_posts.html"
    paginate_by = 8


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comment.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comment.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(self.request, 'Comment successfully added')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )


class AddPost(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView):
    """This view is used to allow logged in users to create a post"""
    form_class = PostForm
    template_name = 'add_post.html'
    success_message = "%(calculated_field)s was created successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of post.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        This function overrides the get_success_message method to add
        the post title into the success message.
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class UserPost(LoginRequiredMixin, generic.ListView):
    """
    Displays list of posts created by a logged in
    user.
    """
    model = Post
    template_name = 'user_post.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return Post.objects.filter(author=self.request.user)


class UpdatePost(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView
        ):
    """
    This view enables logged in users to edit their own posts
    """
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'
    success_message = "%(calculated_field)s was edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        A signed in user is set as the author of the post.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Block user from updating other's posts
        """
        post = self.get_object()
        return post.author == self.request.user

    def get_success_message(self, cleaned_data):
        """
        Override the get_success_message() method to add the post title
        into the success message.
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class DeletePost(
    LoginRequiredMixin,
    UserPassesTestMixin, generic.DeleteView):
    """
    This view enables logged in users to delete their own posts.
    """
    model = Post
    template_name = 'delete_post.html'
    success_message = "Post deleted successfully"
    success_url = reverse_lazy('home')

    def test_func(self):
        """
        Prevent another user from deleting other's post
        """
        post = self.get_object()
        return post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Displays sucess message and cannot be used in generic.DeleteView.


        """
        messages.success(self.request, self.success_message)
        return super(DeletePost, self).delete(request, *args, **kwargs)


class UpdateComment(LoginRequiredMixin, generic.UpdateView):
    """
    Enables logged in users to edit their own comments
    """
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    success_message = "Comment edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the comment.
        """
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from editing user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """ Return to post detail view when comment updated sucessfully"""
        post = self.object.post
        messages.success(self.request, 'Comment successfully edited')
        return reverse_lazy('post_detail', kwargs={'slug': post.slug})


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    This view is used to allow logged in users to delete their own comments
    """
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"

    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display success message given
        SuccessMessageMixin cannot be used in generic.
        """
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to post detail view when comment deleted sucessfully"""
        post = self.object.post

        return reverse_lazy('post_detail', kwargs={'slug': post.slug})


class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
    
class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    template_name = 'user_profile.html'

    def __str__(self,):
         return  f"UserProfile {self.user}by{self.bio}"

    
class AboutPage(generic.TemplateView):
    template_name = "about.html"
