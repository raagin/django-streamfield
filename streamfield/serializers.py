# -*- coding: utf-8 -*-
from rest_framework import serializers

def get_serializer_class(model, base=serializers.ModelSerializer):
    model_ = model

    class Meta:
        model = model_
        fields = '__all__'

    attrs = dict(
        Meta = Meta,
        )

    return type(str(model.__name__ + 'Serializer'), (base, ), attrs)