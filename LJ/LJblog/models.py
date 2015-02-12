from datetime import datetime
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse

class Comment(EmbeddedDocument):
    name = StringField(max_length=200, required=True)
    comment_text = StringField(required=True)
    posted_date = DateTimeField(default=datetime.now)


class Post(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(max_length=200, required=True)
    text = StringField(required=True)
    text_length = IntField()
    date_modified = DateTimeField(default=datetime.now)
    is_published = BooleanField()

    tags = ListField()
    comments = ListField(EmbeddedDocumentField(Comment))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.text_length = len(self.text)
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    def get_edit_url(self):
        return reverse('update', args=[self.id])

    def get_delete_url(self):
        return reverse('delete', args=[self.id])

    def get_comments(self):
        return reverse('comment', args=[self.id])

    def save_comment(self, *args, **kwargs):
        self.text_length = len(self.text)
        return super(Post, self).save(*args, **kwargs)


