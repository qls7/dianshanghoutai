from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """FDFS自定义文件存储类"""
    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL

        self.base_url = base_url

    def _save(self, name, content):
        """
        name: 上传文件的名称
        content: 包含上传文件内容的File对象，content.read()获取上传文件内容
        """
        # 创建fdfs-cli对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fdfs系统
        res = client.upload_by_buffer(content.read())
        # 判断是否上传成功
        if res.get('Status') != 'Upload successed.':
            raise Exception('文件上传FDFS失败')
        # 返回文件id
        file_id = res.get('Remote file_id')
        return file_id

    def exists(self, name):
        """
        判断上传文件的名称和文件系统中原有的文件名是否冲突
        name: 上传文件的名称
        """
        return False

    def url(self, name):
        return self.base_url + name
