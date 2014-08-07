from django.contrib import admin
import reversion
from cis.models import User


class UserAdmin(reversion.VersionAdmin):
    pass

admin.site.register(User, UserAdmin)
