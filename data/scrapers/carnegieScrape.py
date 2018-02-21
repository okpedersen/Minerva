import requests

def main():

	# iterate through pages
	for page in range(1, 300):

		url = 'https://www.cs.cmu.edu/~spok/grimmtmp/'+str(page).zfill(3)+'.txt'

		# request page
		r = requests.get(url)
		# check existence
		if(r.status_code != 200):
			continue
		
		# open file
		filename = 'text'+str(page)+'.txt'
		f = open('text/'+filename, 'w')

		# isolate text from page
		page_text = r.text
		
		f.write(page_text)
	
		# close file
		f.close()

		print(filename)

if __name__ == "__main__":
	main()
