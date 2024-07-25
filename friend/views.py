from django.shortcuts import render
from django.http import HttpResponse
import random


# Create your views here.
def say_hello(request):
    return HttpResponse("hello")


def talking():
    dialog = [
        "안녕! 오늘도 왔구나?",
        "반가워! 난 댕댕이야!",
        "오늘의 날씨는 비가 예상됩니다. 우산을 지참하셔야 하겠습니다.",
        "약 드셨나요?",
    ]
    talk = dialog[random.choice]
