import sys
from web3 import Web3

from_address, to_address, amount, port, pass_phrase = sys.argv[1:]
if from_address and to_address and amount:
    print("Build new transaction by params from_address=%s  to_address=%s amount=%s port=%s."
          % (from_address, to_address, amount, port))


def main():
    ws = Web3(Web3.HTTPProvider("http://localhost:%s" % port))

    check_sum_from_address = Web3.toChecksumAddress(from_address)
    check_sum_to_address = Web3.toChecksumAddress(to_address)

    balance = ws.eth.getBalance(check_sum_from_address)

    if float(balance) < float(amount):
        print("insufficient amount for this transaction, balance=%s, amount=%s" % (balance, amount))
        return

    amount_wei = Web3.toWei(amount, 'ether')
    print("wei amount=%s ." % amount_wei)
    # amount_bytes = Web3.toBytes(amount_wei)
    # amount_hex = Web3.toHex(amount_bytes)
    txn_params = {
        'from': check_sum_from_address,
        'to': check_sum_to_address,
        'value': amount_wei,
        'gas': 21000,
        'gasPrice': ws.eth.gasPrice,
    }
    print(txn_params)

    txn_hash = ws.personal.sendTransaction(txn_params, pass_phrase)
    # txn_hash 类型是 class 'hexbytes.main.HexBytes'
    receipt = ws.eth.waitForTransactionReceipt(txn_hash, 360)
    print("Transaction is successfully submitted! The receipt is : ")
    print("transaction hash : %s. and status is : %s" % (txn_hash, receipt['status']))
    print(receipt)
    # print(txn_params)


if __name__ == '__main__':
    main()
