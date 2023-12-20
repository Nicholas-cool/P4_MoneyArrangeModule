from django.http import HttpResponse
import sqlite3


def e_modify_money_transfer_record(request):
    """ 修改 资金转移记录条目 """

    record_id = request.POST.get('record_id')
    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_from_position = request.POST.get('record_from_position')
    record_to_position = request.POST.get('record_to_position')
    record_amount = request.POST.get('record_amount')
    record_fee = request.POST.get('record_fee')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    ''' money_transfer_record 信息修改到数据库 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取原记录信息
    cur.execute("""SELECT POSITION, INOUT, AMOUNT, FEE FROM money_record WHERE id = '%s';""" % record_id)
    before_position, before_inout, before_amount, before_fee = cur.fetchone()

    # money_position 数据库数额更新（原记录退回）
    before_position_from, before_position_to = before_position.split('&&')

    cur.execute(""" SELECT NAME_EN, MONEY FROM money_position WHERE NAME_EN = '%s'; """ % before_position_from)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before + float(before_amount) + float(before_fee), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), before_position_from))

    cur.execute(""" SELECT NAME_EN, MONEY FROM money_position WHERE NAME_EN = '%s'; """ % before_position_to)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before - float(before_amount), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), before_position_to))

    # 修改记录信息
    cur.execute("""
        UPDATE money_record SET
        NAME = '%s',
        TYPE = '%s',
        AMOUNT = '%s',
        INOUT = '%s',
        POSITION = '%s',
        DESCRIPTION = '%s',
        DATE_STR = '%s',
        FEE = '%s',
        STATUS = 'good'
        WHERE id = '%s';
    """ % (record_name, '转移', record_amount, 'transfer', record_from_position + '&&' + record_to_position,
           record_desc, record_date, record_fee, record_id))
    conn.commit()

    # money_position 数据库数额更新（新增记录）
    cur.execute(""" SELECT NAME_EN, MONEY FROM money_position WHERE NAME_EN = '%s'; """ % record_from_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before - float(record_amount) - float(record_fee), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), record_from_position))

    cur.execute(""" SELECT NAME_EN, MONEY FROM money_position WHERE NAME_EN = '%s'; """ % record_to_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before + float(record_amount), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s'
    """ % (str(money_after), record_to_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('Money Transfer Record 信息修改成功 ！')
