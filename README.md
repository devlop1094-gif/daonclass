# 다온 클래스 (Daon Class)

YTORY 스타일 강의 판매 사이트

## 핵심 흐름
1. 회원가입 / 로그인
2. 강의 구매 → 카카오뱅크 입금 안내
3. 관리자가 입금 확인 후 「결제완료 처리」
4. 구매자가 **내 강의** 메뉴에서 PDF 다운로드

## 주요 기능
- 강의 상품 목록 / 상세
- 회원가입 / 로그인 / 마이페이지
- 카카오뱅크 입금 안내
- **내 강의** 페이지에서 PDF 다운로드
- 관리자 주문 관리

## 로컬 실행
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env에 Gmail, 카카오뱅크 계좌 정보 입력

python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_products
python manage.py runserver
```

## 환경변수 예시
```
EMAIL_HOST_USER=kimsiwoo0214@gmail.com
EMAIL_HOST_PASSWORD=앱비밀번호16자리
BANK_NAME=카카오뱅크
BANK_ACCOUNT=3333-XX-XXXXXXX
BANK_HOLDER=홍길동
SITE_URL=https://your-app.onrender.com
```

## Render 배포
1. GitHub 푸시
2. Render → Web Service 생성
3. Environment Variables 입력
4. Deploy 후:
   ```
   python manage.py createsuperuser
   python manage.py create_sample_products
   ```
