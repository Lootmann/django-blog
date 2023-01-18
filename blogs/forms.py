from django import forms

from blogs.models import Blog


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "content", "is_public")


class BlogUpdateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "content", "is_public")
