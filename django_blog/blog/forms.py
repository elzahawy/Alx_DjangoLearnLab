from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='')

    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    tags_field = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'django, python, tech'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_field'].initial = ", ".join(
                t.name for t in self.instance.tags.all()
            )
