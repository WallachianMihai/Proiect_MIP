from django.contrib import admin
from .models import Question, Answer, Topic, Comment

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Topic)
admin.site.register(Comment)