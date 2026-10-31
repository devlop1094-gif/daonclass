import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '입금 대기'),
        ('paid', '결제 완료'),
        ('cancelled', '취소됨'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='구매자'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='강의'
    )
    status = models.CharField('상태', max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.PositiveIntegerField('결제 금액')
    order_id = models.CharField('주문번호', max_length=64, unique=True, blank=True)
    
    created_at = models.DateTimeField('주문일', auto_now_add=True)
    paid_at = models.DateTimeField('결제일', null=True, blank=True)

    class Meta:
        verbose_name = '주문'
        verbose_name_plural = '주문들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.product.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"DAON-{timezone.now().strftime('%Y%m%d')}-{secrets.token_hex(6).upper()}"
        super().save(*args, **kwargs)

    def mark_as_paid(self):
        """결제 완료 처리"""
        if self.status == 'paid':
            return
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()
