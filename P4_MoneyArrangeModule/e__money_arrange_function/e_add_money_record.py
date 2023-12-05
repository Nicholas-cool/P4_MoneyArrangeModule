from django.http import HttpResponse
import sqlite3


def e_add_money_record(request):
    """ 添加 资金记录条目 到数据库中 """

    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_inout = request.POST.get('record_inout')
    record_type = request.POST.get('record_type')
    record_position = request.POST.get('record_position')
    record_amount = request.POST.get('record_amount')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    ''' money_record 信息添加到数据库 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 添加记录信息
    cur.execute(""" 
        INSERT INTO money_record (NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR) 
        VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, (record_name, record_type, record_amount, record_inout, record_position, record_desc, record_date))
    conn.commit()

    ''' money_position 数据库数额更新 '''
    cur.execute(""" select NAME_EN, MONEY from money_position where NAME_EN = '%s'; """ % record_position)
    money_before = float(cur.fetchone()[1])

    if record_inout == 'in':
        money_after = round(money_before + float(record_amount), 2)
    elif record_inout == 'out':
        money_after = round(money_before - float(record_amount), 2)

    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), record_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('Money Record 信息添加成功 ！')
