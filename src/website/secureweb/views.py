from django.http import HttpResponse
from django.shortcuts import render

# ===================
# View: /secureweb/
# ===================
def home(request):
    return render(request, "secureweb/home.html")


# ============================
# View: /secureweb/playground
# ============================
def playground(request):
    return render(request, "secureweb/playground.html")


# ============================
# View: /secureweb/error
# ============================
def error(request):
    return render(request, "secureweb/error.html")


