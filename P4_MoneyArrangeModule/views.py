from django.shortcuts import render

''' 读取主题配置文件 '''
from .theme_package.common_theme import CommonTheme


# 04_money_arrange
def money_arrange(request):
    return render(request, '04_money_arrange_module/04_money_arrange.html', {'theme': CommonTheme.dark_theme})


# 04_money_arrange_update
def money_arrange_update(request):
    return render(request, '04_money_arrange_module/04_money_arrange_update.html', {'theme': CommonTheme.dark_theme})
