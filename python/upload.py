import easywebdav
import os

#从环境变量中获取webdav的配置
webdav_host=os.environ.get('WEBDAV_URL')
webdav_username=os.environ.get('WEBDAV_USERNAME')
webdav_password=os.environ.get('WEBDAV_PASSWORD')

local_file_path = './tools/123.zip'
remote_file_path = '/123.zip'

# 检查凭据是否都已设置
# 配置信息有一个是空就退出
if not all([webdav_host, webdav_username, webdav_password]):
    print("错误: WebDAV 凭据环境变量未设置。")
    exit(1)








def upload_to_webdav(local_file_path, remote_file_path):
    
    host = webdav_host.replace('https://', '').replace('http://', '')
    protocol = 'https' if webdav_url.startswith('https://') else 'http'
    try:
        webdav = easywebdav.Client(
            host=webdav_host,
            username=webdav_username,
            password=webdav_password,
            protocol='https' 
        )

        # 从远程路径中提取目录部分 检测远程目录是否存在，不存在则创建
        remote_dir = os.path.dirname(remote_file_path)
        if not webdav.exists(remote_dir):
            webdav.mkdir(remote_dir)   
            print(f"创建远程目录: {remote_dir}")
        else:
            print(f"远程目录已存在: {remote_dir}")      
        
        webdav.upload(local_file_path, remote_file_path)
        print(f"文件已上传到 WebDAV: {remote_file_path}")
    


    except Exception as e:
        print(f"上传失败: {e}")
    
if __name__ == "__main__":
    upload_to_webdav(local_file_path, remote_file_path) 



