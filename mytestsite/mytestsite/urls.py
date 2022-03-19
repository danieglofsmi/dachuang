from django.urls import re_path
from mytestsite import views as view1
from django.conf.urls import include
from myapp import views as view2
urlpatterns = [
    re_path('output/', view1.index_out),
    re_path('input/', view2.index_in),
    re_path('app/',include("myapp.urls")),
]