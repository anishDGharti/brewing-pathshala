from django.urls import path
from ..views import base_category_views

urlpatterns = [
    path('base-categories/', base_category_views.BaseCategoryApiView.as_view(), name='base-categories'),
    path('base-categories/<slug:base_category_slug>/', base_category_views.BaseCategoryApiView.as_view(), name='change-category')
]