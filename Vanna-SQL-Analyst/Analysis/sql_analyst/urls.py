
from django.urls import path
from .views import sql_analyst_api

urlpatterns = [
    path("sql-analyst/", sql_analyst_api, name="sql_analyst_api"),
]
