from django.db import models

from user.models import User as UserModel

class Post(models.Model):
    """
        게시글 모델
    """

    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목" , max_length=128)
    content = models.TextField("내용", max_length=50000)
    created_date = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveSmallIntegerField("조회수", default=0)

    is_active = models.BooleanField("활성화 여부", default=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Like(models.Model):
    """
        좋아요 모델
    """
    
    user = models.ForeignKey(UserModel, verbose_name="등록자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.post.title} - {self.user.username}"


class Hashtag(models.Model):
    """
        해시태그 모델
    """

    name = models.CharField("해시태그명", max_length=128)
    post = models.ManyToManyField(Post, verbose_name="게시글", through="PostHashtag")

    def __str__(self):
        return f"{self.id} - {self.name}"

class PostHashtag(models.Model):
    """
        게시글 - 해시태그 중간 테이블
    """

    hashtag = models.ForeignKey(Hashtag, verbose_name="해시태그", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.post.title} - {self.hashtag.name}"