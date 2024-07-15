from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.views.generic import TemplateView
from blog.forms import CreateCommentForm, SignUpForm, CreateBlogPostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post


class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            posts = Post.objects.filter(
                title__icontains=query
            )
        else:
            posts = Post.objects.all()
        
        context = {
            "posts": posts,
            "query": query
        }
        return render(request, self.template_name, context)


class SignUpPageView(TemplateView):
    __doc__ = """ This endpoint shows the SignUp page """
    template_name = "auth/signup.html"

    def get(self, request, *args, **kwargs):
        # if the user is logged in redirecting user to appropriate view via login
        if request.user.is_authenticated:
            return redirect("/login")

        signup_form = SignUpForm()
        context = {"signup_form": signup_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, "Signup Successful! Please login into your account!")
            return redirect("/login")
        else:
            messages.error(
                request, "Signup failed. Please correct the errors below."
            )
        context = {"signup_form": signup_form}
        return render(request, self.template_name, context)


class LoginPageView(TemplateView):
    __doc__ = """This view shows the Login Page"""
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect("/")

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_login_data = authenticate(
            request, username=email, password=password
        )

        if user_login_data:
            login(request, user_login_data)
            return redirect("/")
        else:
            error_message = "Email or Password is Incorrect"
            context = {
                "email": email,
                "error_message": error_message,
            }

        return render(request, self.template_name, context)


class LogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class CreateBlogPostView(LoginRequiredMixin, TemplateView):
    __doc__ = "This view is to create blog post"
    template_name = "blog/create_post.html"

    def get(self, request, *args, **kwargs):
        create_post_form = CreateBlogPostForm()
        context = {
            "form": create_post_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        create_post_form = CreateBlogPostForm(request.POST)

        if create_post_form.is_valid():
            create_form_data = create_post_form.save(commit=False)
            create_form_data.author = request.user
            create_form_data.save()
            return redirect("/")

        context = {
            "form": create_post_form
        }

        return render(request, self.template_name, context)


class CreateComment(LoginRequiredMixin, TemplateView):
    template_name = 'blog/create_comment.html'
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        context['post'] = post
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.id)  
        return self.render_to_response(self.get_context_data(form=form))