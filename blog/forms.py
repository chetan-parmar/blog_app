from django.contrib.auth.forms import UserCreationForm
from blog.models import Comment, User, Post
from django import forms
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': "••••••••",
            'aria-describedby': 'passwordHelpBlock',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': "••••••••",
            'aria-describedby': 'passwordHelpBlock',
        })
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                    'type': 'text',
                    'placeholder': "First Name",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                    }),
            "last_name": forms.TextInput(attrs={
                    'type': 'text',
                    'placeholder': "Last Name",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                    }),
            "email": forms.TextInput(attrs={
                    'type': 'email',
                    'placeholder': "name@example.com",
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                    }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _("Your password must contain at least 8 characters, including both letters and numbers, at least one uppercase letter, and at least one special character.")
        self.fields['password2'].help_text = _("Enter the same password as before, for verification.")


class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category"
        ]

        widgets = {
                "title": forms.TextInput(attrs={
                        'type': 'text',
                        'placeholder': "Title",
                        'class': 'leading-none text-gray-900 p-3 focus:outline-none focus:border-blue-700 mt-4 bg-gray-100 border rounded border-gray-200',
                        }),
                "category": forms.Select(attrs={
                        'type': 'select',
                        'placeholder': "Title",
                        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                        }),
                "content": forms.Textarea(attrs={
                        'type': 'text',
                        'class': 'h-40 text-base leading-none text-gray-900 p-3 focus:oultine-none focus:border-blue-700 mt-4 bg-gray-100 border rounded border-gray-200',
                        }),
            }


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Your Name',
                'class': 'leading-none text-gray-900 p-3 focus:outline-none focus:border-blue-700 mt-4 bg-gray-100 border rounded border-gray-200',
            }),
            'body': forms.Textarea(attrs={
                'type': 'text',
                'placeholder': 'Your Comment',
                'class': 'h-40 text-base leading-none text-gray-900 p-3 focus:outline-none focus:border-blue-700 mt-4 bg-gray-100 border rounded border-gray-200',
            }),
        }