import requests
from common_utils.common_methods import publish_message
from common_utils.env_settings import *

def proxy():
    proxy = requests.get(PROXY_URL).text
    proxies = {
        # 'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    return proxies


def main():
    url = 'https://crates.io/api/v1/crates?page=1&per_page=100&sort=new'
    payload = {'api_key': 'a9dd9f7af76ecd5c56d7f4c3b06ab9b9', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)
    if response.status_code == 200:
        packages_name = response.json().get('crates')
        url_data = []
        for p in packages_name:
            package_name = p.get('id', '')
            url = 'https://crates.io/api/v1/crates/{}'.format(package_name)
            url_data.append(url)
        url_data = list(set(url_data))
        with open('new_package.txt', 'r', encoding='utf-8') as f:
            new_packages = f.readlines()
        new_packages = [x.strip() for x in new_packages]
        for package in url_data[::]:
            if package in new_packages:
                print(f'{package}该包已经在记录中,移除队列')
                url_data.remove(package)
            else:
                with open('new_package.txt', 'a', encoding='utf-8') as f:
                    f.write(package + '\n')
        publish_message('cargo', 'info_add', 'list', url_data)

    else:
        print(response.status_code)
        print('接口访问失败')


if __name__ == '__main__':
    main()
