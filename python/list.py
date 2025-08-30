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

def list_root_contents():
    """测试 WebDAV 连接并列出根目录下所有内容。"""
    try:
        print("正在测试 WebDAV 连接并列出根目录下的所有内容...")
        
        root_contents = client.list('/')
        
        print("\n连接成功！根目录下的文件/文件夹列表如下：")
        
        for item in root_contents:
            if 'href' in item:
                # 打印出完整的相对路径，包括文件名
                print(f"- {item['href']}")
            elif 'name' in item:
                print(f"- {item['name']}")
                
        print("\n--------------------")
        return True
    except Exception as e:
        print("WebDAV 连接失败或读取权限不足！")
        print(f"详细错误信息：{e}")
        return False

if __name__ == "__main__":
    list_root_contents()
