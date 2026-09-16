from django.views.generic import TemplateView


class home(TemplateView):
    template_name = "home.html"

class login(TemplateView):
    template_name = "login.html"  

class register(TemplateView):
    template_name = "register.html"    

class userdashboard(TemplateView):
    template_name = "user/dashboard.html"


class providerdashboard(TemplateView):
    template_name = "provider/dashboard.html"



