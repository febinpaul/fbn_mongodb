from bson import ObjectId
from django import forms
from models import *

class CommentForm(forms.Form):
    name = forms.CharField(max_length=255)
    comment_text = forms.CharField(widget=forms.widgets.Textarea())

    # mytext = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        # if self.instance:
        #     self.fields['name'].initial = self.instance.comments
        #     self.fields['comment_text'].initial = self.instance.comments

    def save(self, commit=True):
        post = self.instance if self.instance else Post()
        comment_dict = Comment(name=self.name,comment_text=self.comment_text)
        # comment_dict['comment_text'] =  Comment(comment_text=self.comment_text)
        # comment_data = Post(comments=[comment_dict])

        print comment_dict
        post.comments.append(comment_dict)
        if commit:
            post.save_comment()

        print post
        return post


class PostForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.widgets.Textarea())
    is_published = forms.BooleanField(required=False)

    # mytext = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['text'].initial = self.instance.text
            self.fields['is_published'].initial = self.instance.is_published


    def save(self, commit=True):
        post = self.instance if self.instance else Post()
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.is_published = self.cleaned_data['is_published']

        print "hello"

        if len(post.tags) > 0:
            del post.tags[:]

        for value in self.tag:
            post.tags.append(value)

        if commit:
            post.save()

        return post

    


