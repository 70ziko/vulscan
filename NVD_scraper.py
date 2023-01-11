import requests
import subprocess
import os
import json
from bs4 import BeautifulSoup

def get_installed_software():
    installed_software = []
    output = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE)

    output_str = output.stdout.decode('utf-8')
    lines = output_str.split('\n')

    for line in lines:
        columns = line.split()
        if len(columns) > 1 and columns[0] == 'ii':
            installed_software.append([columns[1],columns[2]])

    return installed_software

def search_NVD(installed_software):
    packages = [sublist[0] for sublist in installed_software]
    versions = [sublist[1] for sublist in installed_software]

    for software in packages:
        search_url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=" + software
    
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')        
        vulnerabilities = soup.find_all('a')
        
    if vulnerabilities:
        print("Podatności dla programu " + software + ":")
        for vulnerability in vulnerabilities:
            print(vulnerability.text)
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
        url = f'https://vuldb.com/?api&package={name}&version={version}'
        response = json.loads(requests.get(url, headers=headers).text)
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

def main():
    installed_software = get_installed_software()
    vuldb_search(installed_software[:10])

if __name__ == "__main__":
    main()
