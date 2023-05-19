from rest_framework import serializers


class ValuesUFSerializer(serializers.Serializer):
    date = serializers.DateField(format="%Y/%m/%d")
    value = serializers.DecimalField(decimal_places=2, max_digits=30)
