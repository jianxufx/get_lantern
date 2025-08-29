import os
from webdav3.client import Client

# 从环境变量中获取 WebDAV 配置
webdav_url = os.environ.get('WEBDAV_URL')
webdav_username = os.environ.get('WEBDAV_USERNAME')
webdav_password = os.environ.get('WEBDAV_PASSWORD')

local_file_path = './tools/123.zip'
remote_file_path = '/Documents/doc/123.zip'

# 检查凭据是否都已设置
if not all([webdav_url, webdav_username, webdav_password]):
    print("错误: WebDAV 凭据环境变量未设置。")
    exit(1)

# 配置 webdavclient3 客户端
options = {
    'webdav_hostname': webdav_url,
    'webdav_login': webdav_username,
    'webdav_password': webdav_password
}
client = Client(options)

def ensure_remote_dir_exists(client, path):
    """
    检查远程路径中的所有目录，并逐级创建不存在的目录。
    """
    remote_dir = os.path.dirname(path)
    if remote_dir in ('', '/'):
        return

    # 移除首尾斜杠，然后按斜杠分割
    path_parts = remote_dir.strip('/').split('/')
    current_path = ''
    for part in path_parts:
        current_path = current_path + '/' + part
        try:
            
            if not client.exists(current_path):
                client.mkdir(current_path)
                print(f"已创建远程目录: {current_path}")
        except Exception as e:
            print(f"创建远程目录失败: {e}")
            raise

def upload_to_webdav(local_file_path, remote_file_path):
    if not os.path.exists(local_file_path):
        print(f"错误: 本地文件不存在: {local_file_path}")
        exit(1)

    try:
        # 确保目录存在
        ensure_remote_dir_exists(client, remote_file_path)

        # 上传文件
        client.upload_sync(remote_path=remote_file_path, local_path=local_file_path)
        print(f"文件已上传到 WebDAV: {remote_file_path}")

    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    upload_to_webdav(local_file_path, remote_file_path)
