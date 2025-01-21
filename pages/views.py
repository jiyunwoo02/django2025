from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inquiry
from django.contrib import messages

def mainpage(request):
    return render(request, 'pages/mainpage.html')

def company(request):
    return render(request, 'pages/company_info.html')

def support(request):
    return render(request, 'pages/supportpage.html')

def submit_inquiry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 데이터베이스에 저장 -> admin 페이지에서 확인
        Inquiry.objects.create(name=name, email=email, message=message)

        # 성공 메시지
        messages.success(request, "⭕ 문의가 성공적으로 접수되었습니다.")
        return redirect('/support/')
    else:
        # 오류 메시지
        messages.error(request, "❌ 잘못된 요청입니다. 다시 시도해주세요.")
        return redirect('/support/')