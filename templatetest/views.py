from django.shortcuts import render

# Create your views here.


def menu1(request):
    return render(request, 'menu1.html')


def menu2(request):
    s = 'haha'
    return render(request, 'menu2.html', {'s1': s})


def menu3(request):
    return render(request, 'menu3.html')


def base(request):
    return render(request, 'base.html')


def safe_value(request):
    context = {'value': '<script>alert("hello");</script>'}
    return render(request, 'menu3.html', locals())
