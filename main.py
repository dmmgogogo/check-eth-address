import time
import itertools
from web3 import Web3
from eth_utils.exceptions import ValidationError

provider = Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/JCNCAmqFfaWQ9WQrW143reOVrnRg1YfY') # Web3 提供者
web3 = Web3(provider)
web3.eth.account.enable_unaudited_hdwallet_features()

with open('english.txt', 'r') as file: # 讀取 BIP-39 字庫
  mnemonics = file.read().splitlines()

for words in itertools.product(mnemonics, repeat=12): # 產生所有可能的助記詞組合
  mnemonic = ' '.join(words)

  print('------------------------------')
  print(f'助記詞：{mnemonic}')
  
  try:
    account = web3.eth.account.from_mnemonic(
      mnemonic,
      account_path="m/44'/60'/0'/0/0"
    )
    balance = web3.eth.get_balance(account.address)
    balance_ether = web3.from_wei(balance, 'ether')                          
    
    print(f'地址： {account.address}') # 印出地址
    print(f'私鑰： {account.key.hex()}') # 印出私鑰
    print(f'以太餘額：{balance_ether}') # 印出餘額

    if balance_ether != 0: # 帳戶有錢的狀況
      with open('log.txt', 'a') as file:
        file.write(f'助記詞：{mnemonic}\n地址： {account.address}\n私鑰： {account.key.hex()}\n以太餘額：{balance_ether}\n')
        print(f'😎發現含有餘額的帳戶！，已記錄至log.txt😎')
  except ValidationError:
    print('此助記詞校驗和不符。')

  print('------------------------------\n')
  time.sleep(1)
