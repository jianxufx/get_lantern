import easywebdav
import os

try:
    basestring
except NameError:
    basestring = str

#从环境变量中获取webdav的配置
webdav_url=os.environ.get('WEBDAV_URL')
webdav_username=os.environ.get('WEBDAV_USERNAME')
webdav_password=os.environ.get('WEBDAV_PASSWORD')

host = webdav_url.replace('https://', '').replace('http://', '')
protocol = 'https' if webdav_url.startswith('https://') else 'http'

local_file_path = './tools/123.zip'
remote_file_path = '/123.zip'

# 检查凭据是否都已设置
# 配置信息有一个是空就退出
if not all([webdav_url, webdav_username, webdav_password]):
    print("错误: WebDAV 凭据环境变量未设置。")
    exit(1)



def ensure_remote_dir_exists(client, path):
    """
    检查远程路径中的所有目录，并逐级创建不存在的目录。
    """
    # 如果路径是根目录或空，无需操作
    remote_dir = os.path.dirname(path)
    if remote_dir in ('', '/'):
        return

    # 移除首尾的斜杠，然后按斜杠分割
    path_parts = remote_dir.strip('/').split('/')
    current_path = '/'
    for part in path_parts:
        current_path = current_path.rstrip('/') + '/' + part
        
        # 检查当前路径是否存在，不存在则创建
        try:
            if not client.exists(current_path):
                client.mkdir(current_path)
                print(f"已创建远程目录: {current_path}")
        except easywebdav.Error as e:
            # 捕获 WebDAV 错误，例如权限问题
            print(f"创建远程目录失败: {e}")
            raise # 重新抛出异常，停止执行




def upload_to_webdav(local_file_path, remote_file_path):
    
    if not os.path.exists(local_file_path):
        print(f"错误: 本地文件不存在: {local_file_path}")
        exit(1)


    try:
        webdav = easywebdav.Client(
            host=host,
            username=webdav_username,
            password=webdav_password,
            protocol=protocol
        )

        # 从远程路径中提取目录部分 检测远程目录是否存在，不存在则创建
        ensure_remote_dir_exists(webdav, remote_file_path)
        
        webdav.upload(local_file_path, remote_file_path)
        print(f"文件已上传到 WebDAV: {remote_file_path}")
    


    except Exception as e:
        print(f"上传失败: {e}")
    
if __name__ == "__main__":
    upload_to_webdav(local_file_path, remote_file_path) 



