"""
토스페이먼츠 가상계좌 연동
공식 문서: https://docs.tosspayments.com/
"""
import requests
import base64
from django.conf import settings


class TossPayments:
    BASE_URL = "https://api.tosspayments.com/v1"

    def __init__(self):
        self.secret_key = settings.TOSS_SECRET_KEY
        # Basic 인증: secret_key + ":"
        auth_str = f"{self.secret_key}:"
        self.headers = {
            "Authorization": "Basic " + base64.b64encode(auth_str.encode()).decode(),
            "Content-Type": "application/json",
        }

    def create_virtual_account(self, order):
        """
        가상계좌 발급
        order: Order 인스턴스
        """
        url = f"{self.BASE_URL}/virtual-accounts"
        
        payload = {
            "amount": order.amount,
            "orderId": order.order_id,
            "orderName": order.product.title[:100],  # 최대 100자
            "customerName": order.user.username,
            "bank": "카카오",  # 기본 은행 (나중에 선택 가능하게 변경 가능)
            "validHours": 24,  # 24시간 유효
            "customerEmail": order.user.email or "",
        }

        response = requests.post(url, json=payload, headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "virtual_account": data.get("virtualAccount", {}).get("accountNumber", ""),
                "bank_code": data.get("virtualAccount", {}).get("bankCode", ""),
                "bank_name": data.get("virtualAccount", {}).get("bank", ""),
                "due_date": data.get("dueDate"),
                "payment_key": data.get("paymentKey", ""),
                "raw": data,
            }
        else:
            return {
                "success": False,
                "error": response.json() if response.content else response.text,
                "status_code": response.status_code,
            }

    def confirm_payment(self, payment_key, order_id, amount):
        """결제 승인 (웹훅에서 사용하거나 수동 확인용)"""
        url = f"{self.BASE_URL}/payments/confirm"
        payload = {
            "paymentKey": payment_key,
            "orderId": order_id,
            "amount": amount,
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=10)
        return response.json() if response.content else {}
