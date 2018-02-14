import requests

def main():

	# prepare csv
	f = open('texts.txt', 'w')

	# iterate through pages
	for page in range(1, 300):
		url = 'https://www.cs.cmu.edu/~spok/grimmtmp/'+str(page).zfill(3)+'.txt'

		# request page
		r = requests.get(url)
		if(r.status_code != 200):
			continue
		
		# isolate text from page
		page_text = r.text
		
		f.write(page_text)
	
	# close text file
	f.close()

if __name__ == "__main__":
	main()
