from django.urls import path
from blog.views import (CreateComment, HomePageView, SignUpPageView, LoginPageView,
                        LogoutView, CreateBlogPostView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpPageView.as_view(), name='signup'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/post/', CreateBlogPostView.as_view(), name='create_post'),
    path('post/<uuid:post_id>/comment/', CreateComment.as_view(), name='create_comment'),
    # path('register/', register, name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('profile/', profile, name='profile'),
    # path('post/create/', views.create_post, name='create_post'),
    # path('category/create/', views.create_category, name='create_category'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    # path('post/<int:pk>/edit/', edit_post, name='edit_post'),
]
