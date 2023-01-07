import requests
import subprocess
import xmltodict

def get_installed_software():
  installed_software = []
  output = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE)

  output_str = output.stdout.decode('utf-8')
  lines = output_str.split('\n')

  for line in lines:
    columns = line.split()
    if len(columns) > 1 and columns[0] == 'ii':
      installed_software.append(columns[1])

  return installed_software

def main():
    installed_software = get_installed_software()

    for software in installed_software:
        search_url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=" + software
    
    response = requests.get(search_url)
    
    if response.status_code == 200:
        xml_data = xmltodict.parse(response.text)
        
        vulnerabilities = xml_data['nvd']['entry']
        
        if vulnerabilities:
            print("Podatności dla programu " + software + ":")
            for vulnerability in vulnerabilities:
                print(" - " + vulnerability['title'])
    else:
        print("Nie znaleziono podatności dla programu " + software)

if __name__ == "__main__":
    main()
