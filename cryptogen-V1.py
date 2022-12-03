"""
    cryptogen V1
    by ktnk
    tg channel: @cryptogen_btc
    tg profile: @kotenok_1337
"""

import hdwallet as libw
from hdwallet.symbols import BTC, LTC, DASH, ZEC, DOGE
from requests import get as httpget
from requests.exceptions import ConnectionError, ReadTimeout
from json import loads as json
from json.decoder import JSONDecodeError

def addr_balance(network: [BTC, LTC, DASH, ZEC, DOGE], address: str):
	try:
		return json(httpget(f'https://chain.so/api/v2/get_address_balance/{network}/{address}').text)['data']['confirmed_balance']
	except ConnectionError:
		print('requests.exceptions.ConnectionError: please check your Internet connection.')
		return None
	except JSONDecodeError:
		print('json.decoder.JSONDecodeError: something went wrong with JSON decoder, skipping.')
		return None
	except ReadTimeout:
		print('requests.exceptions.ReadTimeout: failed to read.')

wbtc = libw.HDWallet(symbol = BTC)     # BTC wallet
wltc = libw.HDWallet(symbol = LTC)     # LTC wallet
wdash = libw.HDWallet(symbol = DASH)   # DASH wallet
wzec = libw.HDWallet(symbol = ZEC)     # ZEC wallet
wdoge = libw.HDWallet(symbol = DOGE)   # DOGE wallet

balances = open('balances.log', 'a')

while True:
	try:
		mnemonic = libw.utils.generate_mnemonic()
		btcaddr = wbtc.from_mnemonic(mnemonic).p2pkh_address()
		ltcaddr = wltc.from_mnemonic(mnemonic).p2pkh_address()
		dashaddr = wdash.from_mnemonic(mnemonic).p2pkh_address()
		zecaddr = wzec.from_mnemonic(mnemonic).p2pkh_address()
		dogeaddr = wdoge.from_mnemonic(mnemonic).p2pkh_address()
		print(f'Mnemonic: {mnemonic}')
		now = time()
		btcbal = addr_balance(BTC, btcaddr)
		after = time()
		print(after - now)
		print(f'  BTC  :: {btcaddr}  :: {btcbal} BTC')
		ltcbal = addr_balance(LTC, ltcaddr)
		print(f'  LTC  :: {ltcaddr}  :: {ltcbal} LTC')
		dashbal = addr_balance(DASH, dashaddr)
		print(f'  DASH :: {dashaddr}  :: {dashbal} DASH')
		zecbal = addr_balance(ZEC, zecaddr)
		print(f'  ZEC  :: {zecaddr} :: {zecbal} ZEC')
		dogebal = addr_balance(DOGE, dogeaddr)
		print(f'  DOGE :: {dogeaddr}  :: {dogebal} DOGE\n')

		if not btcbal is None:
			if float(btcbal) > 0:
				balances.write(f'{btcaddr} ({mnemonic}) :: {btcbal} BTC\n')
		if not ltcbal is None:
			if float(ltcbal) > 0:
				balances.write(f'{ltcaddr} ({mnemonic}) :: {ltcbal} LTC\n')
		if not dashbal is None:
			if float(dashbal) > 0:
				balances.write(f'{dashaddr} ({mnemonic}) :: {dashbal} DASH\n')
		if not zecbal is None:
			if float(zecbal) > 0:
				balances.write(f'{zecaddr} ({mnemonic}) :: {zecbal} ZEC\n')
		if not dogebal is None:
			if float(dogebal) > 0:
				balances.write(f'{dogeaddr} ({mnemonic}) :: {dogebal} DOGE\n')
	except KeyboardInterrupt:
		break

balances.close()