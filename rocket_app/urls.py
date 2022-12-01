"""rocketdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include

from .views import show_admin_custom_page, show_admin_element_custom_page, ElementAPIView, AddElementAPIView, \
    AvgDebtElementAPIView, CountryElementsAPIView, ProductAPIView

urlpatterns = [
    path('admin-custom-page/', user_passes_test(lambda u: u.is_superuser)(show_admin_custom_page)),
    path('admin-custom-page/<int:id>', user_passes_test(lambda u: u.is_superuser)(show_admin_element_custom_page),
         name='element_page'),
    path('api/view-base-elements', ElementAPIView.as_view()),
    path('api/view-base-elements/<int:id>/', ElementAPIView.as_view()),
    path('api/view-product/', ProductAPIView.as_view()),
    path('api/view-product/<int:id>/', ProductAPIView.as_view()),
    path('api/add-link-element', AddElementAPIView.as_view()),
    path('api/avg-debt', AvgDebtElementAPIView.as_view()),
    path('api/from-country', CountryElementsAPIView.as_view()),

]
