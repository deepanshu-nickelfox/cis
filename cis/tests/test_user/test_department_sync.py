from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from model_mommy import mommy
from hr.models import Position


@override_settings(FEATURE_AUTO_SYNC_USER_POSITION_GROUP=True)
class Test(TestCase):

    def test_case_new_user_with_position_and_department(self):
        department = mommy.make(Group)
        position = mommy.make(Position, department=department)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), {department})

    def test_case_new_user_no_position(self):
        user = mommy.make(get_user_model(), position=None)
        self.assertEqual(set(user.groups.all()), set())

    def test_case_new_user_with_position_no_department(self):
        position = mommy.make(Position)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), set())

    def test_case_old_user_new_position_new_department(self):
        department = mommy.make(Group)
        position = mommy.make(Position, department=department)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), {department})

        another_department = mommy.make(Group)
        another_position = mommy.make(Position, department=another_department)
        user.position = another_position
        user.save()
        self.assertEqual(set(user.groups.all()), {another_department})

    def test_case_old_user_change_position_no_department(self):
        department = mommy.make(Group)
        position = mommy.make(Position, department=department)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), {department})

        another_position = mommy.make(Position)
        user.position = another_position
        user.save()
        self.assertEqual(set(user.groups.all()), set())

    def test_case_old_user_delete_position(self):
        department = mommy.make(Group)
        position = mommy.make(Position, department=department)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), {department})

        user.position = None
        user.save()
        self.assertEqual(set(user.groups.all()), set())

    def test_case_position_department_changes(self):
        department = mommy.make(Group)
        position = mommy.make(Position, department=department)
        user = mommy.make(get_user_model(), position=position)
        self.assertEqual(set(user.groups.all()), {department})

        another_department = mommy.make(Group)
        position.department = another_department
        position.save()
        self.assertEqual(set(user.groups.all()), {another_department})
