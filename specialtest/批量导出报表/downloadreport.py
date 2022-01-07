import requests
import os


def export_report(filepath, method, res_url, headers, data=None):
    try:
        result = requests.request(method=method, url=res_url, data=data, headers=headers)
        result_json = result.json()
        execl_name = result_json["data"]
        if execl_name == "[]":
            print("请耐心等待，系统在发布中")
        download_url = f"http://exceltemp.histudy.com/{execl_name}"
        path = os.getcwd()
        print(path)
        with open(f"{filepath}/{execl_name}", 'wb') as f:
            tmp = requests.get(download_url)
            print(tmp)
            f.write(requests.get(download_url).content)
    except Exception as e:
        print(f"失败{e}")
