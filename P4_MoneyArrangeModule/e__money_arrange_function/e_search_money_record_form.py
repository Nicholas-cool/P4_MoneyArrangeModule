from django.http import JsonResponse
import sqlite3
import datetime
import copy


# 确定行结果是否符合 搜索的文本
def correspond(line, search_text, search_start_date, search_end_date,
               search_inout, search_category, search_position):

    # 搜索语句的验证
    if search_text.lower() not in line[1].lower():
        return False

    # 收支类型的验证
    if search_inout != 'all':
        if search_inout != line[4]:
            return False

    # 分类的验证
    if search_category != 'all':
        if search_category != line[2]:
            return False

    # 来源的验证
    if search_position != 'all':
        if (search_position != line[5] and ((search_position + '&&') not in line[5]) and
                (('&&' + search_position) not in line[5])):
            return False

    # 时间范围的验证
    record_date = datetime.datetime.strptime(line[7], '%Y-%m-%d')

    if search_start_date:
        start_date = datetime.datetime.strptime(search_start_date, '%Y-%m-%d')
        if record_date < start_date:
            return False

    if search_end_date:
        end_date = datetime.datetime.strptime(search_end_date, '%Y-%m-%d')
        if record_date > end_date:
            return False

    return True


def e_search_money_record_form(request):
    """ 获取 money_record 的搜索结果，并按照 layui表格 需要的形式返回 """

    # 得到当前页码page，得到每页的数据量limit
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))

    search_text = request.GET.get('search_text')
    search_start_date = request.GET.get('search_start_date')
    search_end_date = request.GET.get('search_end_date')
    search_inout = request.GET.get('search_inout')
    search_category = request.GET.get('search_category')
    search_position = request.GET.get('search_position')

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
        select ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR
        FROM money_record ORDER BY ID DESC;
    """)
    all_record = []
    all_record_query = cur.fetchall()

    # 查询出来的数据，通过匹配筛选并加入结果集
    for line in all_record_query:
        # 如果符合搜索条件，则加入结果集
        if(correspond(copy.deepcopy(line), search_text, search_start_date, search_end_date,
                      search_inout, search_category, search_position)):

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
            }
            all_record.append(record_dic)

    # 分页数据返回
    count = len(all_record)   # 记录总数
    all_record = all_record[(page-1)*limit:page*limit]

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
