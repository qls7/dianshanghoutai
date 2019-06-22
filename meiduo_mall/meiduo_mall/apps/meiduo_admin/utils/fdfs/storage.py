from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """FDFS自定义文件存储类"""
    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _save(self, name, content):
        """
        保存图片操作
        :param name: 上传文件的名称
        :param content: 包含上传文件内容的File对象, content.read()获取上传文件内容
        :return:
        """
        # 创建fdfs-cli对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fdfs系统
        res = client.upload_by_buffer(content.read())
        # 判断是否上传成功
        if res.get('Status') != 'Upload successed.':
            raise Exception('文件上传FDFS失败')
        # 返回文件id
        file_id = res.get('Remote_file_id')
        return file_id

    def exists(self, name):
        return False

    def get_url(self, name):
        return self.base_url + name
