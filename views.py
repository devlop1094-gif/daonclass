from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings

from products.models import Product
from .models import Order


@login_required
def create_order(request, product_id):
    """주문 생성 (카카오뱅크 입금 안내)"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    # 이미 결제 완료된 주문이 있으면 바로 내 강의로
    paid_order = Order.objects.filter(
        user=request.user,
        product=product,
        status='paid'
    ).first()
    if paid_order:
        messages.info(request, '이미 구매한 강의입니다.')
        return redirect('orders:my_courses')

    # pending 주문이 있으면 재사용
    order = Order.objects.filter(
        user=request.user,
        product=product,
        status='pending'
    ).first()

    if not order:
        order = Order.objects.create(
            user=request.user,
            product=product,
            amount=product.price,
        )

    return render(request, 'orders/order_created.html', {
        'order': order,
        'product': product,
        'bank_name': getattr(settings, 'BANK_NAME', '카카오뱅크'),
        'bank_account': getattr(settings, 'BANK_ACCOUNT', ''),
        'bank_holder': getattr(settings, 'BANK_HOLDER', ''),
    })


@login_required
def my_orders(request):
    """내 주문 목록 (입금 대기 + 완료)"""
    orders = Order.objects.filter(user=request.user).select_related('product')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def my_courses(request):
    """내가 구매한 강의 (결제 완료된 것만) - 여기서 PDF 다운로드"""
    orders = Order.objects.filter(
        user=request.user,
        status='paid'
    ).select_related('product')
    return render(request, 'orders/my_courses.html', {'orders': orders})


@login_required
def download_pdf(request, order_id):
    """구매한 강의 PDF 다운로드 (본인만 가능)"""
    order = get_object_or_404(
        Order,
        pk=order_id,
        user=request.user,
        status='paid'
    )

    pdf_file = order.product.pdf_file
    if not pdf_file:
        messages.error(request, '아직 PDF 파일이 등록되지 않았습니다. 관리자에게 문의해주세요.')
        return redirect('orders:my_courses')

    try:
        response = FileResponse(
            pdf_file.open('rb'),
            as_attachment=True,
            filename=pdf_file.name.split('/')[-1]
        )
        return response
    except Exception:
        raise Http404("파일을 찾을 수 없습니다.")
