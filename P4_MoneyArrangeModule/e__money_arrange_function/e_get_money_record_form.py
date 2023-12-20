from django.http import JsonResponse
import sqlite3


def e_get_money_record_form(request):
    """ 获取 money_record 的所有条目信息，并按照 layui表格 需要的形式返回 """

    # 得到 当前页码page、每页的数据量limit
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))

    # 创建数据库连接，返回连接对象conn，返回游标cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取 money_position对应中文信息
    money_position_map = {}
    cur.execute(""" select NAME_EN, NAME from money_position; """)
    for line in cur.fetchall():
        money_position_map[line[0]] = line[1]

    # 查询该记录的信息，返回列表数据
    cur.execute(""" 
        select ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, STATUS
        FROM money_record ORDER BY ID DESC;
    """)
    all_record = []
    all_record_query = cur.fetchall()

    for line in all_record_query:
        if '&&' in line[5]:
            position_str = '&&'.join([money_position_map[_] for _ in line[5].split('&&')])
        else:
            position_str = money_position_map[line[5]]

        record_dic = {
            'id': line[0],
            'name': line[1],
            'type': line[2],
            'amount': line[3],
            'inout': line[4],
            'position': position_str,
            'description': line[6],
            'date': line[7],
            'status': line[8],
        }
        all_record.append(record_dic)

    # 分页数据返回
    count = len(all_record)  # 记录总数
    all_record = all_record[(page - 1) * limit: page * limit]

    # 关闭数据库连接
    cur.close()
    conn.close()

    # 按照Layui表格所需形式准备数据
    response_result = {
      "code": 0,
      "msg": "",
      "count": count,
      "data": all_record
    }
    return JsonResponse(response_result)
