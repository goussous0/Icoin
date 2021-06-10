import requests 
import re 
import random 
from clint.textui import puts , colored 
import pandas as pd 
from tabulate import tabulate
import argparse






GOLDPRICE_URL = 'https://goldprice.org/cryptocurrency-price'


shorter_reg = r";[A-Za-z0-9. ]{1,}\s*\$[0-9,.]{1,}\s*\$[0-9.,]{1,}\s*[0-9,.]{1,}\s*\$[0-9,.]{1,}\s*[-0-9.,]{1,}"


def load_agents():
	with open('agents.txt' , 'r') as f:
		return list(f)


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)



def tickers(agent):
	
	header = {'User-Agent' : agent.replace("b'", "" ).replace("'" , "").replace("\n","") } 

	resp = requests.get(GOLDPRICE_URL, headers=header  )		
	
	result = remove_tags(resp.text)

	lst = re.findall(shorter_reg , result, re.MULTILINE)

	return lst 
	

def pretty_coins(lst ):
	tmp = [] 

	name = [] 
	market_cap = [] 
	price = [] 
	supply = [] 
	volume = [] 
	change = [] 

	for item in lst:
		## if len(item.split()) == 6 
		#single name

		## if len(item.split()) == 7
		#double name

		## if len(item.split()) == 8
		# triple name


		## Market Cap.	Price	Circulating Supply	Volume (24h)	Change (24h)

		line = item.split()
		if len(line) == 6 :
			name.append(line[0].replace(";",""))
			market_cap.append(line[1])
			price.append(line[2])
			supply.append(line[3])
			volume.append(line[4])
			change.append(line[5]+"%") 

		elif len(line) == 7:
			tmp_name = line[0].replace(";", "")
			name_ = f"{tmp_name} {line[1]} "
			

			name.append(name_)
			market_cap.append(line[2])
			price.append(line[3])
			supply.append(line[4])
			volume.append(line[5])
			change.append(line[6]+"%") 

		elif len(line) == 8:

			tmp_name = line[0].replace(";", "")
			name_ = f"{tmp_name} {line[1]} {line[2]}"
			
			name.append(name_)
			market_cap.append(line[3])
			price.append(line[4])
			supply.append(line[5])
			volume.append(line[6])
			change.append(line[7]+"%") 




	coin_data_frame = {
			'Name' : name,
			'Market Cap'  : market_cap,
			'Price'  : price,
			'Supply'   : supply,
			'Volume' : volume,
			'Change': change,
			}
	df = pd.DataFrame(coin_data_frame , columns = [ 'Name' , 'Market Cap', 'Price', 'Supply', 'Volume', 'Change' ])


	#print (df.head(10))

	return df



def draw_table(df):
	puts(colored.cyan(str(tabulate(df, headers = 'keys', tablefmt = 'psql'))))





if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-n",  help="Show first n coins ")
	parser.add_argument("-r" , help="raw csv file to current folder ")
	
	args = parser.parse_args()

	## load User-Agent 
	agent_lst = load_agents()
	## get data from site 
	df = pretty_coins(tickers(agent=random.choice(agent_lst)))

	if args.n:
		draw_table(df.head(int(args.n)))
	elif not args.n :
		draw_table(df)

	if args.r:
		df.to_csv(f'{str(args.r)}.csv')



	#draw_table(df)




