from django.http import JsonResponse
import sqlite3
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path


def e_upload_db(request):
    upload_file = request.FILES['file']  # 获取文件
    # print(upload_file.name)
    # print(upload_file.size)

    ''' 文件临时存储 '''
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'static/tmp'), base_url='static/tmp')

    if fs.exists('tmp_data.db'):
        fs.delete('tmp_data.db')
    fs.save('tmp_data.db', upload_file)

    ''' 数据库内容迁移 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    conn_tmp = sqlite3.connect('static/tmp/tmp_data.db')
    cur_tmp = conn_tmp.cursor()

    # 1、检查旧版数据库表的结构
    old_schema = {}
    cur_tmp.execute(""" select name from sqlite_master where type='table'; """)
    table_name_list = [_[0] for _ in cur_tmp.fetchall()]
    for table_name in table_name_list:
        cur_tmp.execute(""" pragma table_info('%s') """ % table_name)
        col_name_list = [_[1] for _ in cur_tmp.fetchall()]
        old_schema[table_name] = col_name_list
    # print(old_schema)

    v1_0_0_schema = {
        'select_list': ['ID', 'TEMPLATE', 'TYPE', 'DESC', 'DATA'],
        'money_position': ['POSITION_ID', 'NAME', 'NAME_EN', 'MONEY', 'TYPE', 'ADDITION_INFO', 'HIDDEN'],
        'money_record': ['ID', 'NAME', 'TYPE', 'AMOUNT', 'INOUT', 'POSITION', 'DESCRIPTION', 'DATE_STR', 'FEE']
    }
    v1_1_0_schema = {
        'select_list': ['ID', 'TEMPLATE', 'TYPE', 'DESC', 'DATA'],
        'money_position': ['POSITION_ID', 'NAME', 'NAME_EN', 'MONEY', 'TYPE', 'ADDITION_INFO', 'HIDDEN'],
        'money_record': ['ID', 'NAME', 'TYPE', 'AMOUNT', 'INOUT', 'POSITION', 'DESCRIPTION', 'DATE_STR', 'FEE', 'STATUS']
    }

    # 2、匹配某一旧版本的数据库，并执行迁移
    if sorted(old_schema.items()) == sorted(v1_0_0_schema.items()):
        # 删除现有数据库全部内容
        cur.execute(""" delete from select_list; """)
        cur.execute(""" delete from money_position; """)
        cur.execute(""" delete from money_record; """)
        conn.commit()

        # 逐条导入旧数据库数据
        cur_tmp.execute(f""" select ID, TEMPLATE, TYPE, DESC, DATA from select_list; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into select_list (ID, TEMPLATE, TYPE, DESC, DATA) values (?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4]))

        cur_tmp.execute(f""" select POSITION_ID, NAME, NAME_EN, MONEY, TYPE, ADDITION_INFO, HIDDEN 
                             from money_position; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into money_position (POSITION_ID, NAME, NAME_EN, MONEY, TYPE, 
                            ADDITION_INFO, HIDDEN) values (?, ?, ?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))

        cur_tmp.execute(f""" select ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, FEE 
                             from money_record; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into money_record (ID, NAME, TYPE, AMOUNT, INOUT, POSITION, 
                            DESCRIPTION, DATE_STR, FEE) values (?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]))
        conn.commit()
    elif sorted(old_schema.items()) == sorted(v1_1_0_schema.items()):
        # 删除现有数据库全部内容
        cur.execute(""" delete from select_list; """)
        cur.execute(""" delete from money_position; """)
        cur.execute(""" delete from money_record; """)
        conn.commit()

        # 逐条导入旧数据库数据
        cur_tmp.execute(f""" select ID, TEMPLATE, TYPE, DESC, DATA from select_list; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into select_list (ID, TEMPLATE, TYPE, DESC, DATA) values (?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4]))

        cur_tmp.execute(f""" select POSITION_ID, NAME, NAME_EN, MONEY, TYPE, ADDITION_INFO, HIDDEN 
                             from money_position; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into money_position (POSITION_ID, NAME, NAME_EN, MONEY, TYPE, 
                            ADDITION_INFO, HIDDEN) values (?, ?, ?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))

        cur_tmp.execute(f""" select ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, FEE, STATUS 
                             from money_record; """)
        for line in cur_tmp.fetchall():
            cur.execute(""" insert into money_record (ID, NAME, TYPE, AMOUNT, INOUT, POSITION, 
                            DESCRIPTION, DATE_STR, FEE, STATUS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]))
        conn.commit()
    else:
        cur_tmp.close()
        conn_tmp.close()
        cur.close()
        conn.close()
        raise ValueError("旧版数据库表结构不正确")

    cur_tmp.close()
    conn_tmp.close()
    cur.close()
    conn.close()

    fs.delete('tmp_data.db')  # 清除临时文件

    ''' 按照Layui文件上传所需形式准备 返回数据 '''
    response_result = {
        "code": 0,
        "msg": "",
        "data": {
        }
    }
    return JsonResponse(response_result)
