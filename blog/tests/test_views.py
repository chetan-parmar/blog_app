from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.forms import CreateBlogPostForm, SignUpForm
from blog.models import Post
from blog.views import HomePageView

class HomePageViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password'
        )

        # Create test posts associated with the test user
        self.post1 = Post.objects.create(
            title='Test Post 1',
            content='Content of Test Post 1',
            author=self.user
        )

        self.post2 = Post.objects.create(
            title='Another Post',
            content='Content of Another Post',
            author=self.user
        )

    def test_get_without_query(self):
        url = reverse('home')  
        request = RequestFactory().get(url)
        response = HomePageView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)

    def test_get_with_query(self):
        url = reverse('home') + '?q=Test'
        request = RequestFactory().get(url)
        response = HomePageView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.post2.title)  # Ensure 'Another Post' is not in response
        self.assertNotContains(response, 'Another Post')    # Check for the title explicitly, instead of relying on the self.post2 object


class SignUpPageViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.user_data = {
            'email': 'test@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }
        self.invalid_user_data = {
            'email': 'invalidemail',
            'password1': 'short',
            'password2': 'short'
        }

    def test_get_signup_page(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')
        self.assertIsInstance(response.context['signup_form'], SignUpForm)


class LoginPageViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password'
        )

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_get_login_page_redirect_authenticated_user(self):
        # Authenticate the user
        self.client.login(email='testuser@example.com', password='password')
        
        # Access the login page again
        response = self.client.get(self.login_url)
        
        # Check that the authenticated user is redirected to '/'
        self.assertRedirects(response, '/')

    def test_post_login_page_valid_credentials(self):
        # Prepare valid login data
        login_data = {
            'email': 'testuser@example.com',
            'password': 'password'
        }
        
        # Post the login data
        response = self.client.post(self.login_url, login_data, follow=True)
        
        # Check for successful login and redirection to '/'
        self.assertRedirects(response, '/')
        self.assertTrue(response.context['user'].is_authenticated)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.client.force_login(self.user)  # Simulate user login

    def test_logout_view(self):
        # Ensure the user is initially logged in
        self.assertTrue(self.user.is_authenticated)

        # Access the logout URL
        response = self.client.get(self.logout_url)

        # Check for successful redirection to the home page
        self.assertRedirects(response, '/')
        
        # Verify the user is logged out
        user = getattr(response.wsgi_request, 'user', None)
        self.assertFalse(user.is_authenticated)

   
class CreateBlogPostViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_post_url = reverse('create_post')
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.client.force_login(self.user)  # Simulate user login

        # Form data for creating a post
        self.post_data = {
            'title': 'Test Post',
            'content': 'Content of Test Post',
        }

    def test_get_create_post_page(self):
        response = self.client.get(self.create_post_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_post.html')
        self.assertIsInstance(response.context['form'], CreateBlogPostForm)

    def test_post_create_post_valid_data(self):
        response = self.client.post(self.create_post_url, self.post_data)
        
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful post creation
        self.assertRedirects(response, '/')
        
        # Verify that the post was created
        self.assertTrue(Post.objects.filter(title=self.post_data['title']).exists())
        created_post = Post.objects.get(title=self.post_data['title'])
        self.assertEqual(created_post.author, self.user)

    def test_post_create_post_invalid_data(self):
        invalid_post_data = {
            'title': '',  
            'content': 'Content of Test Post',
        }
        response = self.client.post(self.create_post_url, invalid_post_data)

        self.assertEqual(response.status_code, 200) 
        self.assertFormError(response, 'form', 'title', 'This field is required.')

        
        self.assertFalse(Post.objects.filter(title=invalid_post_data['title']).exists())
