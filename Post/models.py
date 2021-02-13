from author.decorators import with_author
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

@with_author
class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    # content = models.TextField(blank=True, verbose_name='Контент')
    content = RichTextUploadingField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата Создание')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')
    photo = models.ImageField(upload_to='%y%m%d', verbose_name='Фото', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Публиковано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Категория')
    #author  = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Автор')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    @property
    def number_of_comments(self):
        return Comments.objects.filter(post_connected=self).count()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-create_date']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Comments(models.Model):
    post_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + ', ' + self.post_connected.title[:40]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ['-date_posted']