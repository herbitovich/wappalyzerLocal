Python tool for local detection of websites' technology stacks using the Wappalyzer browser extension.
NOTE: You should have xvfb installed in your system in order for the tool to function properly.
NOTE: Sometimes, the web driver has enough time to initialize the Wappalyzer extension, but not enough to load the entire page. This can lead to empty POST requests being sent to the server, creating an instance of the URL in the DB, but without populating it with any JSON data. In such cases, consider increasing the --wait argument value to a higher number.

1. Install all the requirements using pip3 install -r requirements.txt
2. Start the local Django server: python server/manage.py runserver
3. Execute the script using python analyze.py -u (--url) <url> to analyze a single URL or python analyze.py -f (--file) <file_name> to analyze all the URLs from a file. You can also specify how long the web driver should wait for each page to load using the -w (--wait) argument.
4. After the scans are done, all the results will be available in the database.
