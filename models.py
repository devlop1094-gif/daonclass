from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField('강의 제목', max_length=200)
    description = models.TextField('강의 설명')
    price = models.PositiveIntegerField('가격 (원)')
    thumbnail = models.ImageField('썸네일', upload_to='products/thumbnails/', blank=True, null=True)
    pdf_file = models.FileField('PDF 파일', upload_to='products/pdfs/', blank=True, null=True)
    is_active = models.BooleanField('판매 중', default=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '강의 상품'
        verbose_name_plural = '강의 상품들'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    def get_price_display(self):
        return f"{self.price:,}원"
