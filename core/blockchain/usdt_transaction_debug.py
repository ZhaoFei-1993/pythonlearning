import bitcoin.rpc, xlrd, sys, datetime
from http import client

from_address = "1KNPxwHyaUun8ECkMyrmEDrMA8GizYAWX6"
fee_address = "1pqkp8BUBpPHizLkfZfW1N87GjBfpPrFN"
property_id = 31
service_name = "omni_funded_send"

config_info = {
    'host': '127.0.0.1',
    'port': 18335,
    'user': 'RCP_USER',
    'pwd': 'RPC_PASSWORD',
}


def main():
    # 需要read的xlsx路径
    # file_path = sys.argv[1]
    # file_path = "/Users/zhangjinyang/Documents/query_result.xlsx"
    usdt_list = [{
        "address": "1pqkp8BUBpPHizLkfZfW1N87GjBfpPrFN",
        "amount": "1000.5"
    }, {
        "address": "1pqkp8BUBpPHizLkfZfW1N87GjBfpPrFN",
        "amount": "1020.5"
    }]

    handle_usdt_records(usdt_list)


def handle_usdt_records(usdt_list):
    bit_coin_rpc_proxy = bitcoin.rpc.Proxy("http://{user}:{pwd}@{host}:{port}".format(**config_info))
    result_dict = {}
    for usdt_record in usdt_list:
        result = bit_coin_rpc_proxy.call(service_name, from_address, usdt_record['address'], property_id,
                                         str(usdt_record['amount']), fee_address)
        result_dict[usdt_record['address']] = result
    return result_dict


if __name__ == '__main__':
    main()
