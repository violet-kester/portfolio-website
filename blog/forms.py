from django import forms
from .models import Comment


class SharePostForm(forms.Form):
    senders_name = forms.CharField(max_length=50, label="Your name")
    # senders_email = forms.EmailField(label="Your email address")
    recipients_email = forms.EmailField(label="Recipient's email address")
    message = forms.CharField(label="Add a message",
                              required=False,
                              widget=forms.Textarea(attrs={'rows': 5}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'location', 'body']
        labels = {
            'name': 'Your name',
            'location': 'Location (optional)',
            'body': 'Comment'}


class SearchForm(forms.Form):
    query = forms.CharField(label=False)
