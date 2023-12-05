from django.http import JsonResponse
import sqlite3
import datetime


def e_money_get_chart03_data(request):
    """ 获取 chart03&04资金饼图 所需的数据 """

    time_scale = request.GET.get('time_scale')
    time_data = request.GET.get('time_data')
    inout_type = request.GET.get('inout_type')

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
    if time_scale == 'given_span':
        d_start_time, d_end_time = time_data.split('#')
        sd_start_time = datetime.datetime.strptime(d_start_time, '%Y-%m-%d')
        sd_end_time = datetime.datetime.strptime(d_end_time, '%Y-%m-%d')

        sd_duration = (sd_end_time - sd_start_time).days
        for sd_idx in range(sd_duration + 1):   # 循环查询范围内日期的 time_record
            date_str = (sd_start_time + datetime.timedelta(days=sd_idx)).strftime('%Y-%m-%d')

            # 查询该天的 money_record
            cur.execute(" select ID, TYPE, AMOUNT FROM money_record WHERE DATE_STR = '%s' AND INOUT = '%s'; "
                        % (date_str, inout_type))
            for item in cur.fetchall():
                d_type, d_amount = item[1], float(item[2])

                # 进行字典项的填充
                if result_dic.get(d_type) is not None:
                    result_dic[d_type]['money_amount'] += d_amount
                else:
                    result_dic[d_type] = {'money_amount': d_amount}

    elif time_scale == 'all':
        # 查询全部的 time_record
        cur.execute("select ID, TYPE, AMOUNT FROM money_record WHERE INOUT = '%s'; " % inout_type)
        for item in cur.fetchall():
            d_type, d_amount = item[1], float(item[2])

            # 进行字典项的填充
            if result_dic.get(d_type) is not None:
                result_dic[d_type]['money_amount'] += d_amount
            else:
                result_dic[d_type] = {'money_amount': d_amount}

    ''' 按照 chart 所需的格式整理数据 '''
    chart_data_list = []
    for key_type in result_dic.keys():
        chart_data_list.append({
            'name': key_type,
            'value': round(result_dic[key_type]['money_amount'], 2),
        })

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(chart_data_list, safe=False)
