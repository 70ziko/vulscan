import argparse
import numpy as np
import scanners

# obsługa programu poprzez argumenty przekazywane w konsoli
parser = argparse.ArgumentParser(description='Program porównujący zainstalowane oprogramowanie z bazą danych podatności \n')
parser.add_argument('--NVD', help='Przeszukaj stronę National Vulnerability Database od NIST', action='store_true')
parser.add_argument('-d','--csv', type=str , help='Przeszukaj lokalną bazę danych w formacie csv, możliwe określenie ścieżki, domyślnie "./allitems.csv"', default="allitems.csv")
parser.add_argument('--vuldb', help='Skorzystaj z VULDB API, aby znaleźć podatności', action='store_true')
parser.add_argument('--list', help='Po prostu wylistuj zainstalowane oprgoramowanie', action='store_true')
parser.add_argument('-v','--verbose', help='Zawrzyj opisy podatności w wyniku', action='store_true')


args=parser.parse_args()

installed_software = scanners.get_installed_software()

def main():
    if args.NVD and args.verbose:
        scanners.search_NVD(installed_software, True)
    elif args.NVD and not args.verbose:
        scanners.search_NVD(installed_software)

    if args.csv:
        scanners.csv_search(installed_software)
        
    if args.vuldb:
        scanners.vuldb_search(installed_software)
    
    if args.list:
        print(installed_software)

if __name__ == "__main__":
    main()