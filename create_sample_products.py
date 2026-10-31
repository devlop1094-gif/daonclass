from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = '샘플 강의 상품 4개 생성'

    def handle(self, *args, **options):
        products = [
            {
                "title": "유튜브 100만 기법",
                "description": """유튜브 채널을 100만 구독자까지 성장시키는 실전 기법 총정리.

• 알고리즘 완전 정복
• 썸네일·제목·인트로 최적화
• 쇼츠 vs 롱폼 전략
• 수익화·협찬 노하우
• 실제 100만 유튜버들의 공통 패턴 분석

초보부터 중급까지 바로 적용 가능한 핵심만 모았습니다.""",
                "price": 99000,
            },
            {
                "title": "1달 300 기법",
                "description": """단 한 달 만에 결과를 만드는 300가지 실전 기법 모음.

• 하루 10분으로 시작하는 루틴
• 콘텐츠·마케팅·수익화 기법 총망라
• 바로 복사해서 쓸 수 있는 템플릿 포함
• 초보도 따라할 수 있는 단계별 가이드

바쁜 직장인·학생도 실천 가능한 구성입니다.""",
                "price": 79000,
            },
            {
                "title": "엑셀 업무 자동화",
                "description": """반복되는 엑셀 업무를 자동화하는 실무 테크닉.

• 기본 함수부터 VBA·파워쿼리까지
• 데이터 정리·보고서 자동 생성
• 매크로로 클릭 한 번에 처리
• 실무에서 바로 쓰는 예제 파일 제공

매일 반복하던 작업을 자동화해서 시간을 아끼세요.""",
                "price": 59000,
            },
            {
                "title": "네이버 블로그 자동화",
                "description": """네이버 블로그 운영을 자동화해서 트래픽과 수익을 만드는 방법.

• 포스팅 자동화 도구 활용법
• 상위노출 키워드 전략
• 이웃·댓글·공감 자동화
• 애드포스트·협찬 수익화 팁
• 실제 자동화된 운영 예시

시간과 노력을 줄이면서도 블로그를 성장시키는 노하우입니다.""",
                "price": 69000,
            },
        ]

        created = 0
        for data in products:
            obj, is_created = Product.objects.get_or_create(
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "price": data["price"],
                    "is_active": True,
                }
            )
            if is_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"생성: {obj.title}"))
            else:
                self.stdout.write(f"이미 존재: {obj.title}")

        self.stdout.write(self.style.SUCCESS(f"\n총 {created}개 상품이 생성되었습니다."))
        self.stdout.write("PDF 파일은 관리자 페이지에서 나중에 업로드하세요.")
