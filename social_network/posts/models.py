from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    image = models.ImageField(verbose_name='photos', upload_to='post/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Пост №{self.id} от {self.author}"

# для доп. задания
# class PostImage(models.Model):
#     ...

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return "Лайк поставлен"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий №{self.id} к посту №{self.post.id}"