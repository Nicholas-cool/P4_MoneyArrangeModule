from django.http import JsonResponse
import sqlite3
import datetime


def e_money_get_chart_history01_data(request):
    """ 获取 chart_history01资金历史折线图 所需的数据 """

    time_scale = request.GET.get('time_scale')
    time_data = request.GET.get('time_data')
    check_position = request.GET.get('check_position')

    # 创建数据库连接，返回连接对象conn，返回游标cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    ''' 查询 time_data 范围中的 money_remain
        result_dic = {
            'time_str': {
                'money_remain': float,
            }
        }
    '''
    result_dic = {}   # 存储查询结果记录的字典

    d_start_time, d_end_time = time_data.split('#')  # 开始和结束的日期
    d_today_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 当前的日期

    sd_start_time = datetime.datetime.strptime(d_start_time, '%Y-%m-%d')
    # sd_end_time = datetime.datetime.strptime(d_end_time, '%Y-%m-%d')
    sd_today_time = datetime.datetime.strptime(d_today_time, '%Y-%m-%d')
    sd_duration = (sd_today_time - sd_start_time).days   # 时间跨度（必须从今天开始往回推）

    if check_position != 'all':
        # 查询得到当前的资金余量
        cur.execute(" select MONEY, NAME from money_position where NAME_EN = '%s'; " % check_position)
        result_dic[d_today_time] = {'money_remain': float(cur.fetchone()[0])}

        # 计算得到每一天的资金余量
        for sd_idx in range(sd_duration-1, -1, -1):   # 循环查询范围内日期的 money_record（逆序）
            date_str = (sd_start_time + datetime.timedelta(days=sd_idx)).strftime('%Y-%m-%d')
            date_str_next = (sd_start_time + datetime.timedelta(days=sd_idx+1)).strftime('%Y-%m-%d')

            result_dic[date_str] = {  # 初始值为后一天的值
                'money_remain': result_dic[date_str_next]['money_remain']
            }

            # 查询该天的 money_record
            cur.execute(""" select ID, AMOUNT, INOUT, POSITION, FEE FROM money_record WHERE DATE_STR = '%s'; 
            """ % date_str_next)
            for item in cur.fetchall():
                money_amount, money_inout, money_position = float(item[1]), item[2], item[3]
                money_fee = float(item[4]) if item[4] else 0

                if money_inout == 'in' and check_position == money_position:
                    result_dic[date_str]['money_remain'] -= money_amount
                elif money_inout == 'out' and check_position == money_position:
                    result_dic[date_str]['money_remain'] += money_amount
                elif money_inout == 'transfer' and ((check_position + '&&') in money_position):
                    result_dic[date_str]['money_remain'] += money_amount + money_fee
                elif money_inout == 'transfer' and (('&&' + check_position) in money_position):
                    result_dic[date_str]['money_remain'] -= money_amount
    else:
        # 查询得到当前的资金余量
        cur.execute(" select MONEY, NAME from money_position; ")
        result_dic[d_today_time] = {'money_remain': 0}
        for line in cur.fetchall():
            result_dic[d_today_time]['money_remain'] += float(line[0])

        # 计算得到每一天的资金余量
        for sd_idx in range(sd_duration-1, -1, -1):   # 循环查询范围内日期的 money_record（逆序）
            date_str = (sd_start_time + datetime.timedelta(days=sd_idx)).strftime('%Y-%m-%d')
            date_str_next = (sd_start_time + datetime.timedelta(days=sd_idx + 1)).strftime('%Y-%m-%d')

            result_dic[date_str] = {  # 初始值为后一天的值
                'money_remain': result_dic[date_str_next]['money_remain']
            }

            # 查询该天的 money_record
            cur.execute(""" select ID, AMOUNT, INOUT, POSITION, FEE FROM money_record WHERE DATE_STR = '%s'; 
            """ % date_str_next)
            for item in cur.fetchall():
                money_amount, money_inout = float(item[1]), item[2]
                money_fee = float(item[4]) if item[4] else 0

                if money_inout == 'in':
                    result_dic[date_str]['money_remain'] -= money_amount
                elif money_inout == 'out':
                    result_dic[date_str]['money_remain'] += money_amount
                elif money_inout == 'transfer':
                    result_dic[date_str]['money_remain'] += money_fee

    ''' 按照 chart 所需的格式整理数据 '''
    result_dic_list = sorted(result_dic.items(), key=lambda x: x[0], reverse=False)
    result_dic_list_filtered = [x for x in result_dic_list if d_start_time <= x[0] <= d_end_time]

    chart_data_dic = {
        'x_data': [x[0] for x in result_dic_list_filtered],
        'y_data': [round(x[1]['money_remain'], 2) for x in result_dic_list_filtered]
    }

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(chart_data_dic)
