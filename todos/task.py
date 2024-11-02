# todos/tasks.py

from celery import shared_task

# from django.core.mail import send_mail

# @shared_task
# def sample_task():
#     print("I succeed to run the celery with redis.")


# @shared_task
# def send_email_task():
#     send_mail(
#         "Test Mail",
#         "congratulations",
#         "yoosunu010@gmail.com",
#         ["yoosunu010@gmail.com"],
#         fail_silently=False,
#     )
#     print("email sending...")


@shared_task
def simple():
    #     target_time = now.replace(
    #         hour=7, minute=30, second=0, microsecond=0
    #     )  # 원하는 특정 시간 설정

    #     # 모델에서 특정 시간에 해당하는 데이터 가져오기
    #     items = YourModel.objects.filter(your_time_field=target_time)
    # from django.utils import timezone
    # from .models import Todo

    # now_utc = timezone.now()  # UTC 기준 시간
    # now_kst = timezone.localtime(now_utc)
    # times = []

    # todos = Todo.objects.all()
    # for todo in todos:
    #     everydays = todo.everydays.all()
    #     for everyday in everydays:
    #         times.append(everyday.time)
    import requests
    from bs4 import BeautifulSoup

    url = "https://www.jbnu.ac.kr/web/news/notice/sub01.do?pageIndex=1&menu=2377"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.find_all("tr")
    print(trs)
