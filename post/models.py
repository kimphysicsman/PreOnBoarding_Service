from django.db import models

from user.models import User as UserModel

class Post(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목" , max_length=128)
    content = models.TextField("내용", max_length=50000)
    created_date = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveSmallIntegerField("조회수", default=0)

    is_active = models.BooleanField("활성화 여부", default=True)

    def __str__(self):
        return f"{self.id} - {self.title}"