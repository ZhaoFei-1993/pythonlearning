import datetime
import xlrd
from xlwt import *
from xlutils.copy import copy
import sys

today_str = datetime.date.today().strftime("%Y-%m-%d")
file_path = sys.argv[1]
target_path = sys.argv[2]


def write_to_excel(demo_two_dimensional_list):
    for i in range(demo_two_dimensional_list.__len__()):

        if i == 0:
            file = Workbook(encoding='utf-8')
            table = file.add_sheet('汇总')
        else:
            workbook = xlrd.open_workbook(target_path)
            file = copy(workbook)
            table = file.get_sheet(0)
        for j in range(demo_two_dimensional_list[i].__len__()):
            table.write(i, j, demo_two_dimensional_list[i][j])
        file.save(target_path)


def read_from_excel():
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


def main():
    print(read_from_excel())


if __name__ == '__main__':
    main()
