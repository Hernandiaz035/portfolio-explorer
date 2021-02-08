#!/usr/bin/env python3.8
# # -*- coding: utf-8 -*-

import requests
import json

_TOKEN = ''


def api_request(request_str):
    response = requests.get(request_str)

    if response.status_code != 200 or response.json()['message'] != 'OK':
        raise Exception('API response invalid: '+ response.json()['message'] + ' >>> ' + response.json()['result'])
    else:
        return response


def get_ether_balance(wallet_addr):
    response = api_request(f'https://api.etherscan.io/api?module=account&action=balance&address={wallet_addr}&tag=latest&apikey={_TOKEN}')
    balance_raw = response.json()['result']
    balance_fmt = balance_raw[:-18] + '.' + balance_raw[-18:]
    balance = float(balance_fmt)
    return balance


def get_erc20_tkn(wallet_addr):
    response = api_request(f'https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_addr}&startblock=0&endblock=999999999&sort=asc&apikey={_TOKEN}')
    txn_dict = dict()
    for txn in response.json()['result']:
        contract = txn['contractAddress']
        txn_dict[contract] = {
            'tokenSymbol': txn['tokenSymbol'],
            'tokenName': txn['tokenName'],
        }

    for ctr in txn_dict.keys():
        response = api_request(f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={ctr}&address={wallet_addr}&tag=latest&apikey={_TOKEN}')
        balance = response.json()['result']
        if balance != '0':
            balance = balance[:-18] + '.' + balance[-18:]
            txn_dict[ctr]['balance'] = balance
        # else:
        #     txn_dict.pop(ctr)

    return txn_dict
