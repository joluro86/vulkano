from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        "home": "/",  
    }
    return render(request, 'index.html', context)


class BreadcrumbMixin:
    home_url = '/'
    breadcrumb_items = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home"] = self.home_url
        context["breadcrumb_items"] = self.breadcrumb_items
        return context