import datetime
import sys
import xlrd
from xlwt import Workbook
from web3 import Web3
from xlutils.copy import copy

file_path = sys.argv[1]
to_address = sys.argv[2]
pass_phrase = sys.argv[3]
eth_url = "http://localhost:19656"
excel_file_exist = 0
target_path = "/data/" + datetime.date.today().strftime("%Y-%m-%d") + "_result.xlsx"


def handle_eth_records(eth_list):
    result_list = ["申请归集日期", "币种", "数量", "交易费用", "hash"]
    write_to_excel(result_list, 0)
    ws = Web3(Web3.HTTPProvider(eth_url))

    for index in range(eth_list.__len__()):

        from_address = eth_list[index]['address']
        amount = eth_list[index]['amount']

        check_sum_from_address = Web3.toChecksumAddress(from_address)
        check_sum_to_address = Web3.toChecksumAddress(to_address)

        balance = ws.eth.getBalance(check_sum_from_address)

        if float(balance) < float():
            print("insufficient amount for this transaction from_address=%s, balance=%s, amount=%s" % (
                from_address, balance, amount))
            return

        amount_wei = Web3.toWei(amount, 'ether')
        amount_bytes = Web3.toBytes(amount_wei)
        amount_hex = Web3.toHex(amount_bytes)
        txn_params = {
            'from': check_sum_from_address,
            'to': check_sum_to_address,
            'value': amount_hex,
            'gas': 21000,
            'gasPrice': ws.eth.gasPrice,
        }
        txn_hash = ws.personal.sendTransaction(txn_params, pass_phrase)
        receipt = ws.eth.waitForTransactionReceipt(txn_hash, 360)
        result_list = [datetime.date.today().strftime("%Y-%m-%d"), "ETH", str(amount), receipt['fee'],
                       txn_hash]
        write_to_excel(result_list, index + 1)

    return result_list


def read_from_excel():
    workbook = xlrd.open_workbook(file_path)
    target_sheet = workbook.sheet_by_index(0)

    eth_list = []

    for index in range(target_sheet.nrows):
        if index == 0:
            continue

        row_values = target_sheet.row_values(index)

        asset_name = row_values[1]
        amount = row_values[2]
        address = row_values[6]

        if "ETH".__eq__(asset_name):
            eth_dic = {
                "amount": amount,
                "address": address
            }
            eth_list.append(eth_dic)
    return eth_list


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


def main():
    eth_list = read_from_excel()
    write_to_excel(handle_eth_records(eth_list))


if __name__ == '__main__':
    main()
