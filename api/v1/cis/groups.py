from django.contrib.auth.models import Group
from rest_framework import serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.RelatedField(many=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
        )


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    model = Group
    serializer_class = GroupSerializer
