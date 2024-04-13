Curl Data Inspector
The Curl Data Inspector is a Python program that uses the curl utility to fetch data from a URL and formats the output in a desired format.

Usage
bash
Copy code
python app.py [options] <url>
Options
--table: Display output in table format.
--lld: Display output in LLD (Low-Level Discovery) format.
<url>: The URL from which data will be fetched.
Examples
Fetch data from the URL http://example.com and display in JSON format:
bash
Copy code
python app.py http://example.com
Fetch data from the URL https://example.com and display in table format:
bash
Copy code
python app.py --table https://example.com
Fetch data from the URL http://example.com and display in LLD format:
bash
Copy code
python app.py --lld http://example.com
Curl Format
The curl format is defined in the curl_format.json file. Make sure this file is present in the same directory as the app.py script and contains the desired format as specified in the documentation.
