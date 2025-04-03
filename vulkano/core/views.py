from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class BreadcrumbMixin:
    home_url = '/'
    breadcrumb_items = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home"] = self.home_url
        context["breadcrumb_items"] = self.breadcrumb_items
        return context