from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'user', 'product', 'status', 'amount', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email', 'product__title', 'order_id']
    readonly_fields = ['order_id', 'created_at']
    actions = ['mark_as_paid_action']

    @admin.action(description='선택한 주문을 결제완료 처리')
    def mark_as_paid_action(self, request, queryset):
        count = 0
        for order in queryset.filter(status='pending'):
            order.mark_as_paid()
            count += 1
        self.message_user(request, f'{count}개 주문을 결제완료 처리했습니다. 구매자가 내 강의에서 다운로드할 수 있습니다.')
