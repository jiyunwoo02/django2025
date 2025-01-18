from django.shortcuts import render, redirect
from django.http import HttpResponse

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

        # 데이터베이스에 저장
        # Inquiry.objects.create(name=name, email=email, message=message)

        return redirect('/support/')
    else:
        return redirect('/support/')