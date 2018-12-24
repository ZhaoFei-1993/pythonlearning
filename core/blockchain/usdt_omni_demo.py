import bitcoin.rpc
import datetime
import sys

method_omni_get_transaction = "omni_gettransaction"
config_info = {
    'host': '127.0.0.1',
    'port': 18335,
    'user': 'RCP_USER',
    'pwd': 'RPC_PASSWORD',
}
usdt_tx_hash = sys.argv[1]


def demo():
    bit_coin_rpc_proxy = bitcoin.rpc.Proxy("http://{user}:{pwd}@{host}:{port}".format(**config_info))
    receipt = bit_coin_rpc_proxy.call(method_omni_get_transaction, usdt_tx_hash)
    result_list = [datetime.date.today().strftime("%Y-%m-%d"), "USDT", receipt["amount"], receipt['fee'], usdt_tx_hash]
    print(receipt)
    print('\n')
    print(result_list)
    return


if __name__ == '__main__':
    demo()

