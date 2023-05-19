from datetime import datetime

from django.urls import path, register_converter

from .views import ValuesUFViewSet


class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')

urlpatterns = [
    path('list/', ValuesUFViewSet.as_view({'get': 'list'}), name='list_values_uf'),
    path('<date:value_date>/', ValuesUFViewSet.as_view({'get': 'retrieve'}), name='value_uf'),
]
