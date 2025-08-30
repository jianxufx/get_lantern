import os
from webdav3.client import Client

# 从环境变量中获取 WebDAV 配置
webdav_url = os.environ.get('WEBDAV_URL')
webdav_username = os.environ.get('WEBDAV_USERNAME')
webdav_password = os.environ.get('WEBDAV_PASSWORD')

if not all([webdav_url, webdav_username, webdav_password]):
    print("错误: WebDAV 凭据环境变量未设置。")
    exit(1)

options = {
    'webdav_hostname': webdav_url,
    'webdav_login': webdav_username,
    'webdav_password': webdav_password
}
client = Client(options)

def test_webdav_connection():
    """仅测试 WebDAV 连接是否成功，不打印文件列表。"""
    try:
        print("正在测试 WebDAV 连接...")
        
        # 尝试列出根目录，如果成功则证明连接和权限正常
        client.list('/')
        
        print("WebDAV 连接和读取权限测试成功！")
        return True
    except Exception as e:
        print("WebDAV 连接失败或读取权限不足！")
        print(f"详细错误信息：{e}")
        return False

if __name__ == "__main__":
    if not test_webdav_connection():
        # 如果连接失败，可以选择在这里退出，防止后续操作
        exit(1)