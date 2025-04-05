import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def send_request(method="GET", url=None, payload=None, headers=None):
    """
    指定されたURLにリクエストを送信し、レスポンスを返します。

    Args:
        method: メソッド
        url (str): 送信先のURL。
        payload (dict, optional): 送信するデータ（辞書型）。Defaults to None.
        headers (dict, optional): ヘッダー情報（辞書型）。Defaults to None.

    Returns:
        requests.Response: レスポンスオブジェクト。
    """
    try:
        if payload is not None:
            data = json.dumps(payload)
        else:
            data = None

        response = requests.request(method=method, url=url, data=data, headers=headers)
        response.raise_for_status()

        return response

    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        if 'response' in locals() and response is not None:
            print("レスポンス:", response.text)
            print("status_code", response.status_code)
        return None

if __name__ == "__main__":
    FGA_API_URL = os.getenv("FGA_API_URL")
    url = f"{FGA_API_URL}/stores"
    payload = {'name': 'FGA_DEMO_STORE'}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENFGA_AUTHN_PRESHARED_KEYS")}'
        }

    response = send_request(method="POST", url=url, payload=payload, headers=headers)

    if response:
        print("POSTリクエスト成功!")
        print("ステータスコード:", response.status_code)
        try:
            print("レスポンス:", response.json())
            # storeのidを保存
            with open(".env",mode="a") as f:
                store_id = response.json()["id"]
                f.write(f"FGA_STORE_ID={store_id}\n")
        except json.JSONDecodeError:
            print("レスポンス (テキスト形式):", response.text)