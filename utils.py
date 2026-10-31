from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_purchase_email(order, token):
    """구매 완료 시 PDF 다운로드 링크 + 일회용 비밀번호 이메일 발송"""
    subject = f"[{settings.SITE_NAME}] 강의 구매가 완료되었습니다 - {order.product.title}"
    
    download_url = f"{settings.SITE_URL}/orders/download/{order.id}/"
    
    context = {
        'order': order,
        'token': token,
        'product': order.product,
        'download_url': download_url,
        'site_name': settings.SITE_NAME,
    }
    
    # 텍스트 버전
    text_content = f"""
안녕하세요, {order.user.username}님!

[{settings.SITE_NAME}] 강의 구매가 완료되었습니다.

강의명: {order.product.title}
결제금액: {order.amount:,}원

아래 링크에서 일회용 비밀번호를 입력하시면 PDF를 다운로드할 수 있습니다.

다운로드 링크: {download_url}
일회용 비밀번호: {token.token}

※ 이 비밀번호는 한 번만 사용할 수 있으며, 다른 사람과 공유하지 마세요.
※ 비밀번호 유효기간: 7일

감사합니다.
{settings.SITE_NAME}
"""
    
    # HTML 버전 (간단하게)
    html_content = f"""
    <h2>강의 구매가 완료되었습니다!</h2>
    <p>안녕하세요, <strong>{order.user.username}</strong>님!</p>
    <p><strong>강의명:</strong> {order.product.title}<br>
    <strong>결제금액:</strong> {order.amount:,}원</p>
    <p>아래 링크에서 일회용 비밀번호를 입력하시면 PDF를 다운로드할 수 있습니다.</p>
    <p><a href="{download_url}" style="background:#4F46E5;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;">PDF 다운로드 하러가기</a></p>
    <p><strong>일회용 비밀번호:</strong> <code style="font-size:18px;background:#f3f4f6;padding:4px 8px;">{token.token}</code></p>
    <p style="color:#ef4444;">※ 이 비밀번호는 <strong>한 번만</strong> 사용할 수 있으며, 다른 사람과 공유하지 마세요.<br>
    ※ 비밀번호 유효기간: 7일</p>
    <p>감사합니다.<br>{settings.SITE_NAME}</p>
    """
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
