from tastypie.exceptions import Unauthorized
from tastypie.authorization import DjangoAuthorization


class ReadRestrictedDjangoAuthorization(DjangoAuthorization):

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)

        if klass is False:
            return []

        permission = '%s.read_%s' % (klass._meta.app_label, klass._meta.model_name)
        if not bundle.request.user.has_perm(permission):
            raise Unauthorized("You are not allowed to access that resource.")

        return object_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        permission = '%s.read_%s' % (klass._meta.app_label, klass._meta.model_name)
        if not bundle.request.user.has_perm(permission):
            raise Unauthorized("You are not allowed to access that resource.")

        return True
