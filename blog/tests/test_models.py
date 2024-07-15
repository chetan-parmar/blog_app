from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Category, Post, Comment
import uuid

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertIsInstance(self.user.id, uuid.UUID)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Django')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Django')
        self.assertIsInstance(self.category.id, uuid.UUID)
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)
        self.assertEqual(str(self.category), 'Django')

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testauthor@example.com', password='password123'
        )
        self.category = Category.objects.create(name='Django')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertIsInstance(self.post.id, uuid.UUID)
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_can_edit(self):
        another_user = User.objects.create_user(
            email='anotheruser@example.com', password='password123'
        )
        self.assertTrue(self.post.can_edit(self.user))
        self.assertFalse(self.post.can_edit(another_user))
        self.assertTrue(self.post.can_edit(self.user))

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testauthor@example.com', password='password123'
        )
        self.category = Category.objects.create(name='Django')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name='Commenter',
            body='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.name, 'Commenter')
        self.assertEqual(self.comment.body, 'This is a test comment.')
        self.assertIsInstance(self.comment.id, uuid.UUID)
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)
        self.assertEqual(str(self.comment), f'Comment by Commenter on {self.post}')
