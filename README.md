Python tool for local detection of websites' technology stacks using the Wappalyzer browser extension.
NOTE: You should have xvfb installed in your system in order for the tool to function properly.

1. Install all the requirements using pip3 install -r requirements.txt
2. Start the local Django server: python server/manage.py runserver
3. Execute the script using python analyze.py -u <url> to analyze a single URL or python analyze.py -f <file_name> to analyze all the URLs from a file. 
4. After the scans are done, all the results will be available in the database.
