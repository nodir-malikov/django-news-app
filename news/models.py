from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата публикации")  # Time will be saved forever even if we edit news
    updated_at = models.DateTimeField(auto_now=True, blank=True,
                                      verbose_name="Обновлено")  # Time will be updated when we edit news
    photo = models.ImageField(max_length=200, upload_to='photos/%Y/%m/%d/', verbose_name="Расположение фото")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано ли?")
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория',
                                    related_name='get_news')
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        # ordering = ['-created_at', 'id']
        ordering = ['-created_at']
