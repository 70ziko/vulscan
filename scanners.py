import requests
import subprocess
import os
import json
# import csv
import re
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from bs4 import BeautifulSoup

colorama_init()

def get_installed_software():   # Funkcja zwracająca zainstalowane paczki oraz ich wersje
    installed_software = []
    output = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE)

    output_str = output.stdout.decode('utf-8')
    lines = output_str.split('\n')

    for line in lines:
        columns = line.split()
        if len(columns) > 1 and columns[0] == 'ii':
            installed_software.append([columns[1],columns[2]])

    return installed_software

def search_NVD(installed_software, v=False): # Funkcja porównująca zainstalowane oprogramowanie ze stroną NVD
    packages = [sublist[0] for sublist in installed_software]
    versions = [sublist[1] for sublist in installed_software]

    for software in packages:
        search_url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=" + software
    
        response = requests.get(search_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')        

        # Znajdź wszystkie wiersze w odpowiedzi HTML
        vuln_rows = soup.find_all('tr', {'data-testid': re.compile('vuln-row-\d+')})

        vulnerabilities = []

        # Wyekstraktuj z każdego wiersza informacje o podatnościach i zapisz do listy
        for row in vuln_rows:
            vuln = {}
            cve = row.find('a', {'data-testid': re.compile('vuln-detail-link-\d+')})
            vuln['cve'] = cve.text if cve else None

            summary = row.find('p', {'data-testid': re.compile('vuln-summary-\d+')})
            vuln['summary'] = summary.text if summary else None

            pub = row.find('span', {'data-testid': re.compile('vuln-published-on-\d+')})
            vuln['published_on'] = pub.text if pub else None

            cvss2 = row.find('span', {'data-testid': re.compile('vuln-cvss2-na-\d+')})
            vuln['cvss2'] = cvss2.text if cvss2 else None

            cvss3 = row.find('span', {'data-testid': re.compile('vuln-cvss3-na-\d+')})
            vuln['cvss3'] = cvss3.text if cvss3 else None

            vulnerabilities.append(vuln)

        # Wypisz wymaluj
        if vulnerabilities:
            print(f"{Fore.CYAN}Podatności dla programu {Fore.LIGHTMAGENTA_EX}{software}{Fore.BLUE}:{Style.RESET_ALL}")
            for vulnerability in vulnerabilities:
                print(f"{Fore.LIGHTRED_EX}{vulnerability['cve']}{Style.RESET_ALL}")
                if v: print(vulnerability['summary'])
        else:
            print("Nie znaleziono podatności dla programu " + software)

def vuldb_search(installed_software):
    # api key zaciągnięty z zmiennej środowiskowej
    api_key = os.environ.get('VULDB_API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")

    vulnerabilities = {}
    for package in installed_software:
        name = package[0]
        version = package[1]
        headers = {'api-key': api_key}
        url = f'https://vuldb.com/?api&package={name}'
        response = json.loads(requests.post(url, headers=headers).text)
        if 'vulnerabilities' in response:
            vulnerabilities[name] = response['vulnerabilities']

    # Print any vulnerabilities found
    if vulnerabilities:
        print('Vulnerabilities found:')
        for package, vulns in vulnerabilities.items():
            print(f'{package}:')
            for vuln in vulns:
                print(f'    {vuln}')
    else:
        print('No vulnerabilities found.')

def csv_search(installed_software):
    pass

# def main():
#     installed_software = get_installed_software()
#     search_NVD(installed_software)

# if __name__ == "__main__":
#     main()
