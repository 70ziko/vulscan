import requests
import subprocess
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


def main():
    installed_software = get_installed_software()
    search_NVD(installed_software)

if __name__ == "__main__":
    main()
