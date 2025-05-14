from django.urls import path
from .views import landing_view, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
   path('', landing_view, name='landing'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

]
