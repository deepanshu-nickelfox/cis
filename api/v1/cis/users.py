from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        help_text='Current password',
        max_length=settings.PASSWORD_MAX_LENGTH,
    )
    password1 = serializers.CharField(
        help_text='New Password',
        max_length=settings.PASSWORD_MAX_LENGTH
    )
    password2 = serializers.CharField(
        help_text='New Password (confirmation)',
        max_length=settings.PASSWORD_MAX_LENGTH
    )

    def validate_current_password(self, attrs, source):
        """
        current password check
        """
        if self.object.has_usable_password():
            if not self.object.check_password(attrs.get("current_password")):
                raise serializers.ValidationError(
                    'Current password is not correct'
                )

        return attrs

    def validate_password2(self, attrs, source):
        """
        password_confirmation check
        """
        password_confirmation = attrs[source]
        password = attrs['password1']

        if password_confirmation != password:
            raise serializers.ValidationError('Password confirmation mismatch')

        return attrs

    def restore_object(self, attrs, instance=None):
        """ change password """
        if instance is not None:
            instance.set_password(attrs.get('password2'))
            return instance

        return get_user_model()(**attrs)


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

    @action()
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.DATA, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': u'Password successfully changed'})
        return Response(serializer.errors, status=400)
