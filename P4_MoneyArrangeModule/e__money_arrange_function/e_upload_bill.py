from django.http import JsonResponse
import pandas as pd
import io


def get_df_wx_new(row, col_name):
    if col_name == 'A_名字':
        return f'[{row["交易类型"]}] [{row["交易对方"]}]'
    elif col_name == 'B_日期':
        return row['交易时间'][:10]
    elif col_name == 'C_收支':
        if row['收/支'] == '收入':
            return 'in'
        elif row['收/支'] == '支出':
            return 'out'
        else:
            return 'transfer'
    elif col_name == 'D_分类':
        return '待定'
    elif col_name == 'E_位置':
        if row['支付方式'] in ['零钱', '/']:
            return 'wechat'
        else:
            return 'unknown'
    elif col_name == 'F_金额':
        return row['金额(元)'][1:]
    elif col_name == 'G_其他描述':
        desc_str = f'[{row["交易时间"][11:]}]'
        if row["商品"] != '/':
            desc_str += f' [{row["商品"]}]'
        if row["备注"] != '/':
            desc_str += f' [{row["备注"]}]'
        return desc_str
    elif col_name == 'A1_源位置':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易类型']:
                return 'wechat'
            else:
                return 'unknown'
    elif col_name == 'A2_目标位置':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '充值' in row['交易类型']:
                return 'wechat'
            else:
                return 'unknown'
    elif col_name == 'A3_金额':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易类型']:
                all_money = float(row['金额(元)'][1:])
                service_fee = float(row['备注'].replace('服务费', '')[1:])
                return round(all_money - service_fee, 2)
            else:
                return 'Nodata'
    elif col_name == 'A4_手续费':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易类型']:
                service_fee = row['备注'].replace('服务费', '')[1:]
                return service_fee
            else:
                return 'Nodata'


def get_df_alipay_new(row, col_name):
    if col_name == 'A_名字':
        return f'[{row["交易分类"]}] [{row["交易对方"]}]'
    elif col_name == 'B_日期':
        return row['交易时间'][:10]
    elif col_name == 'C_收支':
        if row['收/支'] == '收入':
            return 'in'
        elif row['收/支'] == '支出':
            return 'out'
        elif row['交易状态'] == '交易关闭':
            return 'close'
        else:
            return 'transfer'
    elif col_name == 'D_分类':
        return '待定'
    elif col_name == 'E_位置':
        if '花呗' in str(row['收/付款方式']):
            return 'ant_credit_pay'
        elif '工商银行' in str(row['收/付款方式']):
            return 'icbc'
        else:
            return 'unknown'
    elif col_name == 'F_金额':
        return row['金额']
    elif col_name == 'G_其他描述':
        desc_str = f'[{row["交易时间"][11:]}]'
        if str(row["商品说明"]) != 'nan':
            desc_str += f' [{row["商品说明"]}]'
        if str(row["备注"]) != 'nan':
            desc_str += f' [{row["备注"]}]'
        return desc_str
    elif col_name == 'A1_源位置':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易分类']:
                return 'alipay'
            else:
                return 'unknown'
    elif col_name == 'A2_目标位置':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            return 'unknown'
    elif col_name == 'A3_金额':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易分类']:
                all_money = float(row['金额'][1:])
                service_fee = float(row['备注'].replace('服务费', '')[1:])
                return round(all_money-service_fee, 2)
            else:
                return 'Nodata'
    elif col_name == 'A4_手续费':
        if row['收/支'] in ['收入', '支出']:
            return 'Nodata'
        else:
            if '提现' in row['交易分类']:
                service_fee = row['备注'].replace('服务费', '')[1:]
                return service_fee
            else:
                return 'Nodata'


def e_upload_bill(request):
    upload_file = request.FILES['file']  # 获取文件
    # print(upload_file.name)
    # print(upload_file.size)

    bill_source = request.POST.get('bill_source')  # 账单来源
    upload_mode = request.POST.get('upload_mode')  # 上传模式

    if bill_source == 'wechat_bill':
        # 获取到主体数据部分
        file_content = upload_file.read().decode('utf-8')  # 获取文件内容
        # print(file_content)
        wx_content = ''
        for wx_line in file_content.split('\n'):
            wx_content += wx_line + '\n'
            if '---微信支付账单明细列表---' in wx_line:
                wx_content = ''

        # 转换成dataframe格式，并处理成需要的数据
        df_wx = pd.read_csv(io.StringIO(wx_content))

        col_name_new_list = ['A_名字', 'B_日期', 'C_收支', 'D_分类', 'E_位置', 'F_金额', 'G_其他描述',
                             'A1_源位置', 'A2_目标位置', 'A3_金额', 'A4_手续费']
        for col_name_new in col_name_new_list:
            df_wx[col_name_new] = df_wx.apply(lambda x: get_df_wx_new(x, col_name_new), axis=1)

        df_wx = df_wx[col_name_new_list]

        # 原始数据
        origin_data = df_wx.to_dict(orient='records')

        # 用在预览表格中的数据
        table_data = []
        for row_idx, row in df_wx.iterrows():
            table_data.append({
                'id': '△',
                'name': row['A_名字'],
                'date': row['B_日期'],
                'type': row['D_分类'] if row['C_收支'] != 'transfer' else '转移',
                'inout': row['C_收支'],
                'amount': row['F_金额'] if row['C_收支'] != 'transfer' or row['A1_源位置'] != 'wechat' else row['A3_金额'],
                'position': row['E_位置'] if row['C_收支'] != 'transfer' else f"{row['A1_源位置']}&&{row['A2_目标位置']}",
                'description': row['G_其他描述'],
                'status': 'to_be_checked',
            })

    if bill_source == 'alipay_bill':
        file_content = upload_file.read().decode('ansi')  # 获取文件内容
        # print(file_content)
        # 获取到主体数据部分
        alipay_content = ''
        for alipay_line in file_content.split('\n'):
            alipay_content += alipay_line + '\n'
            if '---支付宝' in alipay_line:
                alipay_content = ''

        print(alipay_content)
        # 转换成dataframe格式，并处理成需要的数据
        df_alipay = pd.read_csv(io.StringIO(alipay_content))

        col_name_new_list = ['A_名字', 'B_日期', 'C_收支', 'D_分类', 'E_位置', 'F_金额', 'G_其他描述',
                             'A1_源位置', 'A2_目标位置', 'A3_金额', 'A4_手续费']
        for col_name_new in col_name_new_list:
            df_alipay[col_name_new] = df_alipay.apply(lambda x: get_df_alipay_new(x, col_name_new), axis=1)

        df_alipay = df_alipay[col_name_new_list]
        df_alipay = df_alipay[df_alipay['C_收支'] != 'close']

        # 原始数据
        origin_data = df_alipay.to_dict(orient='records')

        # 用在预览表格中的数据
        table_data = []
        for row_idx, row in df_alipay.iterrows():
            table_data.append({
                'id': '△',
                'name': row['A_名字'],
                'date': row['B_日期'],
                'type': row['D_分类'] if row['C_收支'] != 'transfer' else '转移',
                'inout': row['C_收支'],
                'amount': row['F_金额'] if row['C_收支'] != 'transfer' or row['A1_源位置'] != 'alipay' else row['A3_金额'],
                'position': row['E_位置'] if row['C_收支'] != 'transfer' else f"{row['A1_源位置']}&&{row['A2_目标位置']}",
                'description': row['G_其他描述'],
                'status': 'to_be_checked',
            })

    ''' 按照Layui文件上传所需形式准备 返回数据 '''
    response_result = {
        "code": 0,
        "msg": "",
        "data": {
            "origin_data": str(origin_data),
            "table_data": table_data,
        }
    }
    return JsonResponse(response_result)
