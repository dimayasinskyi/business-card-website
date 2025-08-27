from django.urls import path

from .views import home, ContactCreateView, PortfolioLiveView


app_name = 'author'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('portfolio/', PortfolioLiveView.as_view(), name='portfolio')
]