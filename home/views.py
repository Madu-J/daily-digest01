from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment, Story
from .forms import CommentForm, StoryForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


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
                "story_form": StoryForm()
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
        story_form = StoryForm(data=request.POST)

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
                "comment_form": CommentForm()
            },
        )


class CommentList(LoginRequiredMixin, generic.ListView):
    """
    This view is used to display a list of comments by the logged in
    user.
    """
    model = Post
    template_name = 'my_profile.html'
    paginate_by = 6

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return Comment.objects.filter(author=self.request.user)

    
class AddStory(
    LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """This view is used to allow logged in users to create a story"""
    form_class = StoryForm
    template_name = 'add_story.html'
    success_message = "%(calculated_field)s was created successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the story.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        This function overrides the get_success_message() method to add
        the story title into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.post.title,
        )

    def get_success_url(self):
        return reverse('add_story')


class Story(
    LoginRequiredMixin, generic.ListView):
    """
    This view is used to display a list of story created by the logged in
    user.
    """
    model = Story
    template_name = 'story.html'
    paginate_by = 6

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return Story.objects.filter(user=self.request.user)


class UpdateComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):

    """
    This view is used to allow logged in users to edit their own comments
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

        return reverse_lazy('post_detail', kwargs={'slug': post.slug})


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):

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
        SuccessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
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
