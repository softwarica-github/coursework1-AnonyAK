import subprocess
import requests

def find_subdomains(domain, wordlist):
    subdomains = []
    with open(wordlist, 'r') as f:
        for line in f:
            subdomain = line.strip()
            url = f'http://{subdomain}.{domain}'
            try:
                response = requests.get(url)
                if response.status_code < 400:
                    print(f'[+] Found subdomain: {url}')
                    subdomains.append(url)
            except requests.ConnectionError:
                pass
    return subdomains

def fuzz_urls(domain, wordlist):
    urls = []
    with open(wordlist, 'r') as f:
        for line in f:
            path = line.strip()
            url = f'http://{domain}/{path}'
            try:
                response = requests.get(url)
                if response.status_code < 400:
                    print(f'[+] Found URL: {url}')
                    urls.append(url)
            except requests.ConnectionError:
                pass
    return urls

def check_ping(hostname):
    try:
        output = subprocess.check_output(["ping", "-c", "1", hostname])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    domain = input('Enter the domain: ')
    wordlist_subdomains = input('Enter the subdomain wordlist file path: ')
    wordlist_urls = input('Enter the URL wordlist file path: ')
    
    subdomains = find_subdomains(domain, wordlist_subdomains)
    print('[+] Subdomain scan finished.')
    print(f'[+] Found {len(subdomains)} subdomains.')

    urls = fuzz_urls(domain, wordlist_urls)
    print('[+] URL scan finished.')
    print(f'[+] Found {len(urls)} URLs.')

    filter_status = input('Filter by status (up/down/all): ').lower()
    for subdomain in subdomains:
        if filter_status == 'up':
            if not check_ping(subdomain):
                continue
        elif filter_status == 'down':
            if check_ping(subdomain):
                continue
        print(f'[+] {subdomain} is {"" if check_ping(subdomain) else "not "}up')

if __name__ == '__main__':
    main()
