from django.urls import path
from rest_framework.schemas import get_schema_view
from . import views
from django.views.generic import TemplateView

schema_view = get_schema_view(title='Bhub API')

urlpatterns = [
    path('clientes/api_doc/', schema_view, name='api_doc'),
    path('clientes/swagger-ui/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_doc'}
    ), name='swagger-ui'),
    path('clientes/', views.ClienteView.as_view()),
    path('clientes/<uuid:pk>/', views.ClienteView.as_view()),
    path('clientes/<uuid:pk>/dadosbancarios/', views.DadosBancariosView.as_view()),
    path('clientes/<uuid:pk>/dadosbancarios/<db_id>/', views.DadosBancariosView.as_view(), name='dadosbancarios'),
]