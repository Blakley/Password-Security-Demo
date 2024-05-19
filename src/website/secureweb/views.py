from django.http import HttpResponse

# ===================
# View: /secureweb/
# ===================
def index(request):
    return HttpResponse("Hello, world. You're at the SecureWeb index.")



