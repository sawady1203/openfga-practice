import os
import json
from pprint import pprint
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

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
    FGA_STORE_ID = os.getenv("FGA_STORE_ID")
    url = f"{FGA_API_URL}/stores/{FGA_STORE_ID}/write"
    
    # # tuple.json を読み込んで pyload にする
    # with open("tuple.json", mode="r") as f:
    #     tuple = json.load(f)
    # print(tuple)

    tuple = [
        # 組織: hoge.com の 管理者(org-admin) を sawady として追加
        {
            "user": "user:sawady",
            "relation": "org-admin",
            "object": "organization:hoge.com"
        },
        # 組織 hoge.com の group として hoge-owner-group を 追加
        {
            "user": "group:hoge-owner-group",
            "relation": "group",
            "object": "organization:hoge.com"
        },
        # 組織 hoge.com の group として hoge-editor-group を 追加
        {
            "user": "group:hoge-editor-group",
            "relation": "group",
            "object": "organization:hoge.com"
        },
        # 組織 hoge.com の group として hoge-viewer-group を 追加
        {
            "user": "group:hoge-viewer-group",
            "relation": "group",
            "object": "organization:hoge.com"
        },
        # hoge-owner-group のユーザーとして hoge-owner-man を追加
        {
            "user": "user:hoge-owner-man",
            "relation": "member",
            "object": "group:hoge-owner-group"
        },
        # hoge-editor-group のユーザーとして hoge-editor-man を追加
        {
            "user": "user:hoge-editor-man",
            "relation": "member",
            "object": "group:hoge-editor-group"
        },
        # hoge-viewer-group のユーザーとして hoge-viewer-man を追加
        {
            "user": "user:hoge-viewer-man",
            "relation": "member",
            "object": "group:hoge-viewer-group"
        },
        # hoge-owner-group を owner として hoge-folder に追加
        {
            "user": "group:hoge-owner-group#member",
            "relation": "owner",
            "object": "folder:hoge-folder"
        },
        # hoge-editor-group を editor として hoge-folder に追加
        {
            "user": "group:hoge-editor-group#member",
            "relation": "editor",
            "object": "folder:hoge-folder"
        },
        # hoge-viewer-group を viewer として hoge-folder に追加
        {
            "user": "group:hoge-viewer-group#member",
            "relation": "viewer",
            "object": "folder:hoge-folder"
        },
        # hoge-folder に sample.txt を追加
        {
            "user": "folder:hoge-folder",
            "relation": "parent",
            "object": "file:sample.txt"
        },
        ]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENFGA_AUTHN_PRESHARED_KEYS")}'
        }

    payload = {
        "writes": {
            "tuple_keys": tuple
        },
        "authorization_model_id": os.getenv("FGA_AUTHORIZATION_MODEL_ID")
    }

    pprint(payload)

    response = send_request(method="POST", url=url, payload=payload, headers=headers)

    if response:
        print("ステータスコード:", response.status_code)
        try:
            pprint(response.json(),indent=2)

        except json.JSONDecodeError:
            print("レスポンス (テキスト形式):", response.text)
