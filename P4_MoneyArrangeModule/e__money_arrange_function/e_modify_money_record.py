from django.http import HttpResponse
import sqlite3


def e_modify_money_record(request):
    """ 修改 资金记录条目 到数据库中 """

    record_id = request.POST.get('record_id')
    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_inout = request.POST.get('record_inout')
    record_type = request.POST.get('record_type')
    record_position = request.POST.get('record_position')
    record_amount = request.POST.get('record_amount')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    ''' 数据库信息修改 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取原记录信息
    cur.execute("""SELECT POSITION, INOUT, AMOUNT FROM money_record WHERE id = '%s';""" % record_id)
    before_position, before_inout, before_amount = cur.fetchone()

    # money_position 数据库数额更新（原记录退回）
    before_amount = -1 * float(before_amount) if before_inout == 'in' else before_amount
    cur.execute(""" select NAME_EN, MONEY from money_position where NAME_EN = '%s'; """ % before_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before + float(before_amount), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), before_position))

    # 修改 money_record 记录信息
    cur.execute(""" 
        UPDATE money_record SET
        NAME = '%s',
        TYPE = '%s',
        AMOUNT = '%s',
        INOUT = '%s',
        POSITION = '%s',
        DESCRIPTION = '%s',
        DATE_STR = '%s',
        STATUS = 'good'
        WHERE id = '%s';
    """ % (record_name, record_type, record_amount, record_inout, record_position,
           record_desc, record_date, record_id))
    conn.commit()

    # money_position 数据库数额更新（新增记录）
    record_amount = -1 * float(record_amount) if record_inout == 'out' else record_amount
    cur.execute(""" select NAME_EN, MONEY from money_position where NAME_EN = '%s'; """ % record_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before + float(record_amount), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), record_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('Money Record 信息修改成功 ！')
