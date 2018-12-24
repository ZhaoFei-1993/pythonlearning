import bitcoin.rpc
import datetime
import sys
import xlrd
from xlwt import Workbook
from xlutils.copy import copy

"""
Read me
执行前需要检查的内容有
file_path  生成文件的路径，包含文件名 .txt。 执行python脚本时的第一个参赛
to_address  目标地址，财务提供。 执行python脚本时的第二个参数
fee_address  消耗dust的地址，线上环境
"""

# from_address = "1KNPxwHyaUun8ECkMyrmEDrMA8GizYAWX6"
file_path = sys.argv[1]
to_address = sys.argv[2]

fee_address = "1pqkp8BUBpPHizLkfZfW1N87GjBfpPrFN"
property_id = 31
service_name = "omni_funded_send"
method_omni_get_transaction = "omni_gettransaction"
excel_file_exist = 0
target_path = "/data/" + datetime.date.today().strftime("%Y-%m-%d") + "_result.xlsx"

config_info = {
    'host': '127.0.0.1',
    'port': 18335,
    'user': 'RCP_USER',
    'pwd': 'RPC_PASSWORD',
}


def main():
    # file_path = "/Users/zhangjinyang/Documents/query_result.xlsx"
    usdt_list = read_from_excel(file_path)
    handle_usdt_records(usdt_list)


def read_from_excel(file_path):
    workbook = xlrd.open_workbook(file_path)
    target_sheet = workbook.sheet_by_index(0)

    usdt_list = []

    for index in range(target_sheet.nrows):
        if index == 0:
            continue

        row_values = target_sheet.row_values(index)

        asset_name = row_values[1]
        amount = row_values[2]
        address = row_values[6]

        if "USDT".__eq__(asset_name):
            usdt_dic = {
                "amount": amount,
                "address": address
            }
            usdt_list.append(usdt_dic)
    return usdt_list


def write_to_excel(result_list, row):
    if excel_file_exist == 0:
        file = Workbook(encoding='utf-8')
        table = file.add_sheet('汇总')
    else:
        workbook = xlrd.open_workbook(target_path)
        file = copy(workbook)
        table = file.get_sheet(0)
    for j in range(result_list.__len__()):
        table.write(row, j, result_list[j])
    file.save(target_path)


def handle_usdt_records(usdt_list):
    result_list = ["申请归集日期", "币种", "数量", "交易费用", "hash"]
    write_to_excel(result_list, 0)
    bit_coin_rpc_proxy = bitcoin.rpc.Proxy("http://{user}:{pwd}@{host}:{port}".format(**config_info))

    for index in range(usdt_list.__len__()):
        hash = bit_coin_rpc_proxy.call(service_name, usdt_list[index]['address'], to_address, property_id,
                                       str(usdt_list[index]['amount']), fee_address)
        receipt = bit_coin_rpc_proxy.call(method_omni_get_transaction, hash)
        result_list = [datetime.date.today().strftime("%Y-%m-%d"), "USDT", receipt["amount"], receipt['fee'], hash]
        write_to_excel(result_list, index + 1)


if __name__ == '__main__':
    main()
