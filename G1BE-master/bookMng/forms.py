from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Comment
from .models import MessageBox

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
            'rating',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class MessageForm(ModelForm):
    class Meta:
        model = MessageBox
        fields = [
            'chat',
        ]

