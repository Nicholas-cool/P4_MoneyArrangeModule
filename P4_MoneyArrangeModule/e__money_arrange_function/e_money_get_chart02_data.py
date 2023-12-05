from django.http import JsonResponse
import sqlite3


def e_money_get_chart02_data(request):
    """ 获取 chart02资金饼图 和 chart02a资金柱状图 所需的数据 """

    date_str = request.GET.get('date_str')

    # 创建数据库连接，返回连接对象conn，返回游标cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    ''' 查询 time_data 范围中的
        result_dic = {
            'type': {
                'money_amount': float,
            }
        }
    '''
    result_dic = {}   # 存储查询结果记录的字典

    # 查询该天的 money_record
    cur.execute(" select ID, TYPE, AMOUNT FROM money_record WHERE DATE_STR = '%s' AND INOUT = '%s'; "
                % (date_str, 'out'))
    for item in cur.fetchall():
        d_type, d_amount = item[1], float(item[2])

        # 进行字典项的填充
        if result_dic.get(d_type) is not None:
            result_dic[d_type]['money_amount'] += d_amount
        else:
            result_dic[d_type] = {'money_amount': d_amount}

    # 关闭数据库连接
    cur.close()
    conn.close()

    ''' 按照 chart 所需的格式整理数据 '''
    # chart02所需数据
    chart02_data_list = []
    for key_type in result_dic.keys():
        chart02_data_list.append({
            'name': key_type,
            'value': round(result_dic[key_type]['money_amount'], 2),
        })

    # chart02a所需数据
    chart02a_data_dic = {'yaxis': [], 'data': []}
    sorted_list = sorted(chart02_data_list, key=lambda x: x['value'], reverse=False)

    for item in sorted_list:
        chart02a_data_dic['yaxis'].append(item['name'])
        chart02a_data_dic['data'].append(item['value'])

    return JsonResponse({
        'chart02_data': chart02_data_list,
        'chart02a_data': chart02a_data_dic,
    })
