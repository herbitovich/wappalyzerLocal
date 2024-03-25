from selenium import webdriver
import os, sys, getopt, time, threading, re

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"u:f:",["url=","file=",])
	except getopt.GetoptError:
		print('[*] Usage: python ./analyze.py -u <url> to scan a specific URL or analyze.py -f <file> to scan URLS from a given file')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-u", "--url"):
			print('[!] Reading URL: '+arg)
			url = arg
			static_analyze([url])
		elif opt in ("-f", "--file"):
			print('[!] Reading URLs from file: '+arg)
			file = open(arg,'r').readlines()
			static_analyze(file)

def check_os():
	platform = sys.platform
	if platform == "linux" or platform == "linux2":
		print('[!] Launching ChromeDriver for Linux')
		return '_linux'	
	elif platform == "darwin":
		print('[!] Launching ChromeDriver for Mac')
		return '_mac'
	elif platform == "win32" or platform == "win64":
		print('[!] Launching ChromeDriver for Windows')
		return '.exe'

ext_dir_path = os.getcwd()+'/extensions/' #chrome extensions

def add_ext(options, crx_name):
	crx_path = ext_dir_path + crx_name + '.crx'
	if not os.path.isfile(crx_path):
		raise FileNotFoundError('File not found.')
	options.add_extension(crx_path)

def chrome_new_session(operating_system,extensions=None):
	service = webdriver.ChromeService(executable_path=os.getcwd()+'/chromedriver'+operating_system)
	options = webdriver.ChromeOptions()
	if extensions:
		[add_ext(options, crx) for crx in extensions]
	driver = webdriver.Chrome(service=service, options=options)
	driver.is_occupied = False
	driver.set_page_load_timeout(30)
	return driver
	
drivers = []
threads = []
def load(url):
	global threads,drivers
	freeInd = get_free()
	threads.append(threading.Thread(target=scrape, args=(freeInd, url)))
	threads[-1].driverInd = freeInd
	threads[-1].start()
	drivers[freeInd].is_occupied = True
def scrape(driverInd, url):
	global drivers
	driver = drivers[driverInd]
	try:
		print('[*] Scanning '+url)
		driver.get(url)
		time.sleep(2)
		print('[!] Complete')
	except Exception as e:
		print(f'[!] {e}')
def clean():
	global threads,drivers
	while True:
		for t in threads.copy():
			if not(t.is_alive()):
				drivers[t.driverInd].is_occupied = False
				threads.remove(t)
		time.sleep(0.1)
def get_free():
	global drivers
	free = [ind for ind in range(len(drivers)) if not(drivers[ind].is_occupied)]
	while not free:
		time.sleep(0.1)
		free = [ind for ind in range(len(drivers)) if not(drivers[ind].is_occupied)]
	return free[0]

def static_analyze(urls):
	global threads, drivers
	count = int(input("[?] Quantity of threads: ")) if len(urls)>1 else 1
	cleaner = threading.Thread(target=clean)
	cleaner.start()
	for n in range(count):
		driver = chrome_new_session(extensions=['wappalyzer'],operating_system=check_os())
		drivers.append(driver)
	for url in urls:
		url = url.strip('\r\n')
		url = re.search(r"(?:https?://)?([^:/\n]+)", url).group(1)
		load('https://'+url)
	print("[!] All URLS have been scanned.")
if __name__ == '__main__':
	main(sys.argv[1:])
		
