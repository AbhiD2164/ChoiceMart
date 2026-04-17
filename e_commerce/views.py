from django.shortcuts import render


def error_403(request, exception):
    return render(request, "errors/403.html")


def error_404(request, exception):
    return render(request, "errors/404.html")


def error_405(request, exception):
    return render(request, "errors/405.html")


def error_501(request, exception):
    return render(request, "errors/501.html")