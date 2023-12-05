from django.http import JsonResponse
import sqlite3


def e_get_money_record(request):
    """ 获取 单个资金记录条目 """
    record_id = request.GET.get('record_id')

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取记录信息
    cur.execute(""" 
        SELECT ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, FEE
        FROM money_record WHERE ID = '%s';
    """ % record_id)

    single_record = cur.fetchone()
    single_record_dic = {
        'id': single_record[0],
        'name': single_record[1],
        'type': single_record[2],
        'amount': single_record[3],
        'inout': single_record[4],
        'position': single_record[5],
        'description': single_record[6],
        'date': single_record[7],
        'fee': single_record[8],
    }

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(single_record_dic)
