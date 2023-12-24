from django.http import HttpResponse
import sqlite3


def add_money_record(record_name, record_date, record_inout, record_type, record_position, record_amount,
                     record_desc):

    """ money_record 信息添加到数据库 """
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 添加记录信息
    cur.execute(""" 
        INSERT INTO money_record (NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, STATUS) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (record_name, record_type, record_amount, record_inout, record_position, record_desc,
          record_date, 'to_be_checked'))
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
    return True


def add_money_transfer_record(record_name, record_date, record_from_position, record_to_position,
                              record_amount, record_fee, record_desc):

    """ money_transfer_record 信息添加到数据库 """
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 添加记录信息
    cur.execute(""" 
        INSERT INTO money_record (NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, FEE, STATUS) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
    """, (record_name, '转移', record_amount, 'transfer', record_from_position + '&&' + record_to_position,
          record_desc, record_date, record_fee, 'to_be_checked'))
    conn.commit()

    ''' money_position 数据库数额更新(from账户) '''
    cur.execute(""" select NAME_EN, MONEY from money_position where NAME_EN = '%s'; """ % record_from_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before - float(record_amount) - float(record_fee), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s';
    """ % (str(money_after), record_from_position))
    conn.commit()

    ''' money_position 数据库数额更新(to账户) '''
    cur.execute(""" select NAME_EN, MONEY from money_position where NAME_EN = '%s'; """ % record_to_position)
    money_before = float(cur.fetchone()[1])
    money_after = round(money_before + float(record_amount), 2)
    cur.execute("""
        UPDATE money_position SET
        MONEY = '%s'
        WHERE NAME_EN = '%s';
    """ % (str(money_after), record_to_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()
    return True


def e_upload_money_records(request):
    upload_origin_data = request.POST.get('upload_origin_data')

    ''' 检查是否有 unknown 位置，如果数据库中没有，则添加 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" select NAME, NAME_EN from money_position; """)
    if 'unknown' not in [_[1] for _ in cur.fetchall()]:
        cur.execute(""" insert into money_position (NAME, NAME_EN, TYPE, MONEY, HIDDEN) 
                        values (?, ?, ?, ?, ?); """, ('待定', 'unknown', 'unknown', '0.0', 'no'))
        conn.commit()

    cur.execute(""" select DATA from select_list where TEMPLATE = '%s' and DESC = '%s'; 
                """ % ('04_money_arrange', 'income_category'))
    if '待定' not in [_[0] for _ in cur.fetchall()]:
        cur.execute(""" insert into select_list (TEMPLATE, TYPE, DESC, DATA)
                        values (?, ?, ?, ?)""", ('04_money_arrange', 'select', 'income_category', '待定'))
        conn.commit()

    cur.execute(""" select DATA from select_list where TEMPLATE = '%s' and DESC = '%s'; 
                """ % ('04_money_arrange', 'outcome_category'))
    if '待定' not in [_[0] for _ in cur.fetchall()]:
        cur.execute(""" insert into select_list (TEMPLATE, TYPE, DESC, DATA)
                        values (?, ?, ?, ?)""", ('04_money_arrange', 'select', 'outcome_category', '待定'))
        conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    # print(upload_origin_data)
    for row in reversed(eval(upload_origin_data)):
        if row['C_收支'] == 'transfer':
            if row['A1_源位置'] != 'wechat':
                add_money_transfer_record(row['A_名字'], row['B_日期'], row['A1_源位置'], row['A2_目标位置'],
                                          row['F_金额'], 0, row['G_其他描述'])
            else:
                add_money_transfer_record(row['A_名字'], row['B_日期'], row['A1_源位置'], row['A2_目标位置'],
                                          row['A3_金额'], 0, row['G_其他描述'])
        else:
            add_money_record(row['A_名字'], row['B_日期'], row['C_收支'], row['D_分类'], row['E_位置'],
                             row['F_金额'], row['G_其他描述'])

    return HttpResponse('账单上传成功！')
