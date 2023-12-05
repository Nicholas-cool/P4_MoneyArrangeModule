from django.http import HttpResponse
import sqlite3


def e_delete_money_transfer_record(request):
    """ 删除 资金转移记录条目 """
    record_id = request.GET.get('record_id')

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

    # 删除记录信息
    cur.execute(""" DELETE FROM money_record WHERE id = '%s';""" % record_id)
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('Money Transfer Record 信息删除成功 ！')
