from django.contrib import admin
from blog.models import User, Category, Post, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "id"
    ]
    list_filter = ["is_staff"]
    fieldsets = [
        ("User Credentials", {"fields": [
            "email",
            "password"
            ]}),
        ("Personal info", {"fields":
                           ["first_name",
                            "last_name",
                            ]
                           }),
        ("Permissions", {"fields": [
            "is_staff",
            "is_superuser",
            "is_active",
            "groups",
            "user_permissions"
            ]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)

admin.site.register(Category)

admin.site.register(Post)

admin.site.register(Comment)
