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
            # Definindo o formato diretamente no código
            curl_format_str = '''
                {
                    "time_namelookup": "%{time_namelookup}",
                    "time_connect": "%{time_connect}",
                    "time_appconnect": "%{time_appconnect}",
                    "time_pretransfer": "%{time_pretransfer}",
                    "time_redirect": "%{time_redirect}",
                    "time_starttransfer": "%{time_starttransfer}",
                    "time_total": "%{time_total}",
                    "speed_download": "%{speed_download}",
                    "speed_upload": "%{speed_upload}",
                    "remote_ip": "%{remote_ip}",
                    "remote_port": "%{remote_port}",
                    "local_ip": "%{local_ip}",
                    "local_port": "%{local_port}",
                    "size_download": "%{size_download}",
                    "size_upload": "%{size_upload}",
                    "http_code": "%{http_code}",
                    "content_type": "%{content_type}",
                    "url_effective": "%{url_effective}"
                }
            '''

            # Executa o comando curl e formata a saída como JSON
            curl_output = subprocess.check_output(
                ["curl", self.url, "-w", curl_format_str, "-o", "/dev/null", "-s"], 
                stderr=subprocess.PIPE, 
                universal_newlines=True
            )

            # Converte a saída do curl para um dicionário Python
            self.result = json.loads(curl_output)

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
                    # Extrair a data de expiração
                    expiry_date_str = cert['notAfter']
                    expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
                    # Calcular dias restantes
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

    # Manipula parâmetros
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

    # Exibe o resultado no formato escolhido
    if output_format == "table":
        # Exibe a saída em formato de tabela com seções baseadas nas categorias de informações
        sections = {
            "Timing Information": ["time_namelookup", "time_connect", "time_appconnect", "time_pretransfer", "time_redirect", "time_starttransfer", "time_total"],
            "Transfer Speed Information": ["speed_download", "speed_upload"],
            "IP and Port Information": ["remote_ip", "remote_port", "local_ip", "local_port"],
            "Data Size Information": ["size_download", "size_upload"],
            "SSL Expiration Information": ["expire_date", "days_until_expiration"],
            "Other Information": ["http_code", "content_type", "url_effective"]
        }

        for section_name, section_keys in sections.items():
            section_data = [[key, result.get(key, "")] for key in section_keys]
            print("\n{}:".format(section_name))
            print(tabulate(section_data, headers=["Key", "Value"], tablefmt="grid"))
    elif output_format == "lld":
        # Exibe a saída em formato LLD
        print(json.dumps({"data": [result]}))
    else:
        # Exibe a saída no formato JSON padrão
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
