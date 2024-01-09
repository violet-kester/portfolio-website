from django import forms
from .models import Comment


class SharePostForm(forms.Form):
    senders_name = forms.CharField(
        label='Your name',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    recipients_email = forms.EmailField(
        label="Recipient's email address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Add a message (optional)',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'location', 'body']
        labels = {
            'name': 'Your name',
            'location': 'Location (optional)',
            'body': 'Comment'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }


class SearchForm(forms.Form):
    query = forms.CharField(label=False)
