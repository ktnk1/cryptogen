"""
	cryptogen V2
	by ktnk
	tg channel: @cryptogen_btc
	tg profile: @kotenok_1337
"""

from hdwallet import HDWallet as wallet
from hdwallet.utils import generate_mnemonic
from hdwallet.symbols import BTC
from requests import get as httpget
from requests.exceptions import ConnectionError, ReadTimeout
from json import loads as json
from json.decoder import JSONDecodeError
from tqdm import tqdm
from art import text2art as ascii_art

def addr_balance(address: str):
	try:
		return json(httpget(f'https://chain.so/api/v2/get_address_balance/BTC/{address}').text)['data']['confirmed_balance']
	except ConnectionError:
		print('requests.exceptions.ConnectionError: please check your Internet connection.')
		return None
	except JSONDecodeError:
		print('json.decoder.JSONDecodeError: something went wrong with JSON decoder, skipping.')
		return None
	except ReadTimeout:
		print('requests.exceptions.ReadTimeout: failed to read.')

logo = f"cryptogen\n{ascii_art('V2')}"
print(logo)
wallet = wallet(symbol = BTC)
balances = open('balances.log', 'a')
database = set()
n = 0

with open('base.txt', 'r') as f:
	for line in tqdm(f, desc = "Loading BTC database", unit = " addr"):
		#print(line)
		database.add(line)
	f.close()

while True:
	try:
		n += 1
		wallet.from_mnemonic(generate_mnemonic())

		p2pkh = wallet.p2pkh_address() #1
		if p2pkh in database:
			p2pkh_bal = addr_balance(p2pkh)
			print(f'[{n}] Key: {wallet.private_key()} :: Type: p2pkh :: Balance: {p2pkh_bal}')
			balances.write(f'Key: {wallet.private_key()} :: Type: p2pkh :: Balance: {p2pkh_bal}\n')
		else:
			print(f'[{n}] Key: {wallet.private_key()} :: Type: p2pkh :: Failed')

		p2sh = wallet.p2sh_address() #3
		if p2sh in database:
			p2sh_bal = addr_balance(p2sh)
			print(f'[{n}] Key: {wallet.private_key()} :: Type: p2sh :: Balance: {p2sh_bal}')
			balances.write(f'Key: {wallet.private_key()} :: Type: p2sh :: Balance: {p2sh_bal}\n')
		else:
			print(f'[{n}] Key: {wallet.private_key()} :: Type: p2sh :: Failed')
	except KeyboardInterrupt:
		break

balances.close()