import subprocess
import json
import sys
import datetime
from tabulate import tabulate
import ssl
import socket

class CurlDataFetcher:
    def __init__(self, url):
        self.url = url
        self.result = {}

    def fetch_curl_data(self):
        try:
            # Load curl format from configuration file
            with open("./curl_inform.json", "r") as file:
                curl_format = json.load(file)
            
            # Convert the dictionary to a formatted JSON string
            curl_format_str = json.dumps(curl_format)

            # Execute the curl command and format the output as JSON
            curl_output = subprocess.check_output(
                ["curl", self.url, "-w", curl_format_str, "-o", "/dev/null", "-s"], 
                stderr=subprocess.PIPE, 
                universal_newlines=True
            )

            # Convert curl output to a Python dictionary
            self.result = json.loads(curl_output)

        except FileNotFoundError:
            print("Error: Configuration file 'curl_inform.json' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in 'curl_inform.json': {e}")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            self.result = {"error": "Failed to execute curl", "stderr": e.stderr}
        except Exception as e:
            self.result = {"error": str(e)}

    def fetch_ssl_expiration(self):
        try:
            hostname = self.url.replace('https://', '').replace('http://', '').split('/')[0]
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    # Extract expiration date
                    expiry_date_str = cert['notAfter']
                    expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
                    # Calculate remaining days
                    days_left = (expiry_date - datetime.datetime.utcnow()).days
                    self.result['expire_date'] = expiry_date_str
                    self.result['days_until_expiration'] = days_left
        except Exception as e:
            self.result['ssl_expiration_error'] = str(e)

    def get_result(self):
        return self.result

def print_help():
    print("Usage: {} [--table|--lld] <url>".format(sys.argv[0]))
    print("Options:")
    print("  --table: Display output in table format.")
    print("  --lld: Display output in LLD (Low-Level Discovery) format.")
    print("  <url>: The URL to fetch data from.")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print_help()
        sys.exit(0)

    output_format = "json"
    url = None

    # Handle parameters
    for arg in sys.argv[1:]:
        if arg in ["--table", "--lld"]:
            output_format = arg[2:]
        else:
            url = arg

    if not url:
        print("Error: Missing URL argument.")
        sys.exit(1)

    fetcher = CurlDataFetcher(url)
    fetcher.fetch_curl_data()
    fetcher.fetch_ssl_expiration()
    result = fetcher.get_result()

    # Display the result according to the chosen format
    if output_format == "table":
        # Display output in table format with sections based on "Information" categories
        sections = {
            "Timing Information": ["time_namelookup", "time_connect", "time_appconnect", "time_pretransfer", "time_redirect", "time_starttransfer", "time_total"],
            "Transfer Speed Information": ["speed_download", "speed_upload"],
            "IP and Port Information": ["remote_ip", "remote_port", "local_ip", "local_port"],
            "Data Size Information": ["size_download", "size_upload"],
            "SSL Expiration Information": ["expire_date", "days_until_expiration"],
            "Other Information": ["num_connects", "redirect_url", "ssl_verify_result", "http_code", "content_type", "errormsg", "exitcode", "filename_effective", "ftp_entry_path", "http_connect", "http_version", "method", "num_headers", "num_redirects", "proxy_ssl_verify_result", "referer", "response_code", "scheme", "size_header", "size_request", "stderr", "data", "url", "effective_url", "domain"]
        }

        for section_name, section_keys in sections.items():
            section_data = [[key, result.get(key, "")] for key in section_keys]
            print("\n{}:".format(section_name))
            print(tabulate(section_data, headers=["Key", "Value"], tablefmt="grid"))
    elif output_format == "lld":
        # Display output in LLD format
        print(json.dumps({"data": [result]}))
    else:
        # Display output in default JSON format
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
