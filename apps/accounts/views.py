from django.views.generic import TemplateView
from django.conf import settings

class GoogleCallbackRender(TemplateView):
    template_name = "google_callback.html"

class home(TemplateView):
    template_name = "home.html"

class login(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["google_client_id"] = settings.GOOGLE_OAUTH_CLIENT_ID
        context["google_redirect_uri"] = settings.GOOGLE_OAUTH_CALLBACK_URL        

        return context    

class register(TemplateView):
    template_name = "register.html"    

class userdashboard(TemplateView):
    template_name = "user/dashboard.html"


class providerdashboard(TemplateView):
    template_name = "provider/dashboard.html"

class createbooking(TemplateView):
    template_name = "user/create_booking.html"    

class profile(TemplateView):
    template_name = "user/profile.html"    

class booking_offers(TemplateView):
    template_name = "user/booking_offers.html"       

class my_booking(TemplateView):
    template_name = "user/my_booking.html"      

class rating(TemplateView):
    template_name = "user/rating.html"

class provider_profile(TemplateView):
    template_name = "provider/profile.html"

class request(TemplateView):
    template_name = "provider/request.html"    

class provider_offer(TemplateView):
    template_name = "provider/provider_offer.html"     

class provider_work(TemplateView):
    template_name = "provider/provider_work.html"      

class addservice(TemplateView):
    template_name = "user/add_service.html"       

class userlist(TemplateView):
    template_name = "user/user_list.html"    

class userupdate(TemplateView):
    template_name = "user/user_update.html"   

class userview(TemplateView):
    template_name = "user/user_view.html"    

class selectrole(TemplateView):
    template_name = "select_role.html"

class CustomerDetail(TemplateView):
    template_name = "provider/customer_details.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_id"] = self.kwargs.get("booking_id")
        return context
  