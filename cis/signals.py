from django.conf import settings
from hr.models import Position


def sync_user_groups_when_user_created_with_position(sender, instance, created, **kwargs):
    """
    Auto-assign user to the department group if user is created with position.

    @type instance cis.models.User
    """
    if not settings.FEATURE_AUTO_SYNC_USER_POSITION_GROUP:
        return

    if created:
        if instance.position and instance.position.department:
            instance.groups.add(instance.position.department)


def sync_user_groups_when_position_changes(sender, instance, **kwargs):
    """
    Auto-assign user to the new department group if user is updated and
    position changed.
    De-assign from the previous department.

    @type instance cis.models.User
    """
    if not settings.FEATURE_AUTO_SYNC_USER_POSITION_GROUP:
        return

    from cis.models import User
    if instance.id:
        old_instance = User.objects.get(pk=instance.id)
        if old_instance and old_instance.position and old_instance.position.department:
            if instance.position != old_instance.position or \
                            old_instance.position.department != instance.position.department:
                instance.groups.remove(old_instance.position.department)

        if instance.position and instance.position.department:
            instance.groups.add(instance.position.department)


def admin_department_sync_workaround(sender, instance, action, **kwargs):
    """
    Django admin calls "clear" on groups field, thus nullifying sync signals
    efforts. This is a workaround for it.

    @type instance cis.models.User
    """
    if action == 'post_clear':
        if instance.position and instance.position.department:
            instance.groups.add(instance.position.department)


def sync_user_groups_when_department_changes(sender, instance, **kwargs):
    """
    Auto-assign related users to the department group if position is updated and
    department changed.
    De-assign from the previous department.

    @type instance hr.models.Position
    """
    if not settings.FEATURE_AUTO_SYNC_USER_POSITION_GROUP:
        return

    from cis.models import User
    if instance.id:
        old_instance = Position.objects.get(pk=instance.id)
        old_department = old_instance.department
        new_department = instance.department
        related_users = User.objects.filter(position=instance)
        for related_user in related_users:
            if old_department:
                related_user.groups.remove(old_department)
            if new_department:
                related_user.groups.add(new_department)
