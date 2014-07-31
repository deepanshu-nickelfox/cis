from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    user_permissions = serializers.RelatedField(many=True)
    groups = serializers.RelatedField(many=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'user_permissions',
            'groups',
            'first_name',
            'last_name',
            'middle_name',
            'sex',
            'date_of_birth',
            'is_superuser',
        )


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    model = get_user_model()
    serializer_class = UserSerializer

