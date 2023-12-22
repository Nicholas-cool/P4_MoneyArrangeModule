from django.http import JsonResponse
import sqlite3


def e_get_auto_complete_rules(request):
    """ 从数据库中获取 money_record 的自动填充规则 """

    # 创建数据库连接，返回连接对象conn，返回游标cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    type_list_dic = {}  # 所有收入和支出分类项目
    cur.execute(""" select DATA from select_list where 
                    TEMPLATE = '04_money_arrange' and TYPE = 'select' and DESC = 'income_category'; """)
    type_list_dic['in'] = [_[0] for _ in cur.fetchall()]
    cur.execute(""" select DATA from select_list where 
                    TEMPLATE = '04_money_arrange' and TYPE = 'select' and DESC = 'outcome_category'; """)
    type_list_dic['out'] = [_[0] for _ in cur.fetchall()]

    cur.execute(""" select NAME_EN from money_position; """)
    money_position_list = [_[0] for _ in cur.fetchall()]

    # 获取自动填充规则，并进行合法性检测，忽略不合法的规则
    auto_complete_rule_list = []
    cur.execute(""" select PATTERN, INOUT, TYPE, POSITION, AMOUNT from money_record_auto_complete
                    order by PRIORITY asc; """)
    for line in cur.fetchall():
        if line[1] not in ['in', 'out']:  # 合法性检验-1
            continue
        if line[2] not in type_list_dic[line[1]]:  # 合法性检验-2
            continue
        if line[3] not in money_position_list:  # 合法性检验-3
            continue
        try:
            float(line[4])  # 合法性检验-4
        except:
            continue

        # 通过合法性检验，加入字典
        auto_complete_rule_list.append([line[idx] for idx in range(5)])

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(auto_complete_rule_list, safe=False)
