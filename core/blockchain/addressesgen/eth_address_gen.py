#!/usr/bin/env python
# - generate_eth_series_address.py
# date: 2018-03-11
# version: 1.1
# require: python version >= 3.6
# install web3: pip3 install web3

from web3 import Web3, HTTPProvider
import sys
import datetime

coin_name, totally_accounts = sys.argv[1:]

if coin_name and totally_accounts:
    print("The program will generate %s address of %s." % (totally_accounts, coin_name.upper()))
else:
    print("EXECUTE: python %s COIN_NAME COIN_NUMBER" % sys.argv[0])
    sys.exit(10)

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
output_sql = "%s_address_%s.sql" % (coin_name.lower(), timestamp)
user_password = ""


# INSERT INTO `address_pool_erc20` (`asset_code`, `coin_address`, `wallet_account`, `address_status`, `del_flag`, `create_date`, `update_date`)
# VALUES
#	('ERC20', '0x168b5babfbf515cf83d02d738b4d03eb3bb8f2cd', 'erc20', 'NEW', 'FALSE', now(), now());

def main():
    web_handle = Web3(HTTPProvider('http://localhost:18547'))
    accounts_list = []
    address_sql = 'INSERT INTO `address_pool_' + coin_name.lower() + '` VALUES\n'

    count = 0
    while count < int(totally_accounts):
        account = web_handle.personal.newAccount(user_password)
        if account not in accounts_list:
            address_sql += "(null,'%s', '%s', '%s', 'NEW', 'FALSE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),\n" % (
                coin_name.upper(), account, coin_name.lower())
            # address_sql += "(null, 0, '%s', '', '%s', '%s', 'NEW', 'FALSE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
            # \n" % (coin_name.upper(), account, coin_name.lower())
            accounts_list.append(account)
            count += 1
            print("%d : %s" % (count, account))

    with open(output_sql, 'a+') as f:
        f.write("%s;" % address_sql.strip("\n").strip(","))
    print('finished')


if __name__ == '__main__':
    main()
