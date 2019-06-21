from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultPagination(PageNumberPagination):
    """自定义分页器"""
    # 指定分页默认页容量
    page_size = 5
    # 指定页容量的参数名
    page_size_query_param = 'page_size'
    # 指定最大页容量
    max_page_size = 20

    def get_paginated_response(self, data):
        """
        重写page的返回字段
        :param data:
        :return:
        """
        return Response(OrderedDict([
            ('counts', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))

