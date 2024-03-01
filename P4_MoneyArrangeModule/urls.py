"""P4_MoneyArrangeModule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.urls import re_path
from django.views.generic.base import RedirectView

from . import views

# self define function locations
from .e__money_arrange_function import e_get_money_positions, e_get_money_record_form, e_search_money_record_form, \
    e_add_money_record, e_add_money_transfer_record, e_money_get_chart01_data, e_money_get_chart02_data, \
    e_money_get_chart03_data, e_money_get_chart_history01_data, e_get_money_record, e_modify_money_record, \
    e_delete_money_record, e_modify_money_transfer_record, e_delete_money_transfer_record, e_upload_bill, \
    e_upload_money_records, e_get_auto_complete_rules, e_upload_db

from .y__common_function import y_get_select_list, y_login_view

url_names = [
    # 04_money_arrange_module
    ('e_get_money_positions', e_get_money_positions.e_get_money_positions),
    ('e_get_money_record_form', e_get_money_record_form.e_get_money_record_form),
    ('e_search_money_record_form', e_search_money_record_form.e_search_money_record_form),
    ('e_add_money_record', e_add_money_record.e_add_money_record),
    ('e_get_money_record', e_get_money_record.e_get_money_record),
    ('e_modify_money_record', e_modify_money_record.e_modify_money_record),
    ('e_modify_money_transfer_record', e_modify_money_transfer_record.e_modify_money_transfer_record),
    ('e_delete_money_record', e_delete_money_record.e_delete_money_record),
    ('e_delete_money_transfer_record', e_delete_money_transfer_record.e_delete_money_transfer_record),
    ('e_add_money_transfer_record', e_add_money_transfer_record.e_add_money_transfer_record),
    ('e_money_get_chart01_data', e_money_get_chart01_data.e_money_get_chart01_data),
    ('e_money_get_chart02_data', e_money_get_chart02_data.e_money_get_chart02_data),
    ('e_money_get_chart03_data', e_money_get_chart03_data.e_money_get_chart03_data),
    ('e_money_get_chart_history01_data', e_money_get_chart_history01_data.e_money_get_chart_history01_data),
    ('e_upload_bill', e_upload_bill.e_upload_bill),
    ('e_upload_money_records', e_upload_money_records.e_upload_money_records),
    ('e_get_auto_complete_rules', e_get_auto_complete_rules.e_get_auto_complete_rules),
    ('e_upload_db', e_upload_db.e_upload_db),

    # common部分的函数
    ('y_get_select_list', y_get_select_list.y_get_select_list),
]

urlpatterns = [
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),  # 允许 /media/ 路径访问
    path('favicon.ico', RedirectView.as_view(url=r'static/images/favicon.ico')),  # 网页图标
    path('login/', y_login_view.y_login_view, name='login'),  # 登录功能
    path('logout/', y_login_view.y_logout_view, name='logout'),  # 登出功能

    path('', views.money_arrange),
    path('04money_arrange/', views.money_arrange),
    path('04money_arrange_update/', views.money_arrange_update),
] + [path(url_name+'/', url_view, name=url_name) for url_name, url_view in url_names]
