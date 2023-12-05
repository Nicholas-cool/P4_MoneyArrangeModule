from django.http import JsonResponse
import sqlite3


def y_get_select_list(request):
    """ 获取 特定选择框（select框） 的选项列表 """

    template = request.GET.get('template')
    l_type = request.GET.get('type')
    desc = request.GET.get('desc')

    # 创建数据库连接，返回连接对象conn，返回游标cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    select_list = []
    cur.execute(""" 
        select DATA from select_list 
        where TEMPLATE = '%s' and TYPE = '%s' and DESC = '%s';
    """ % (template, l_type, desc))

    for item in cur.fetchall():
        select_list.append(item[0])

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(select_list, safe=False)  # 传输的为列表类型
