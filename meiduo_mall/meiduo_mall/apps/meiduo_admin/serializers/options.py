from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


# class SpecOptionsSimpleSerializer(serializers.ModelSerializer):
#     """规格简易列表"""
#     class Meta:
#         model = SPUSpecification
#         fields = ('id', 'name')


class SpecOptionsSerializer(serializers.ModelSerializer):
    """规格选项序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    spec = serializers.StringRelatedField(label='规格名称', read_only=True)

    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')

    def validate_spec_id(self, value):
        """校验规格id"""
        if not SPUSpecification.objects.filter(id=value):
            raise serializers.ValidationError('规格id错误')
        return value
