from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from SecurityApp.models import AuditLog, User


class AuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('laura', 'laura@example.com', 'Clave-segura-1')

    def test_roles_are_created_with_their_permissions(self):
        admin = Group.objects.get(name='Administrator')
        codenames = admin.permissions.values_list('codename', flat=True)
        self.assertIn('ban_user', codenames)
        self.assertIn('moderate_content', codenames)
        self.assertEqual(Group.objects.get(name='Member').permissions.count(), 0)

    def test_login_with_username_or_email(self):
        self.assertTrue(self.client.login(username='laura', password='Clave-segura-1'))
        self.client.logout()
        self.assertTrue(self.client.login(username='LAURA@example.com', password='Clave-segura-1'))

    def test_banned_user_cannot_login(self):
        # Un usuario vetado queda inactivo
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.client.login(username='laura', password='Clave-segura-1'))

    def test_register_adds_member_role_and_audit_log(self):
        response = self.client.post(reverse('register'), {
            'username': 'pedro', 'email': 'pedro@example.com',
            'password1': 'Clave-segura-2', 'password2': 'Clave-segura-2',
        })
        self.assertRedirects(response, reverse('profile_form'), fetch_redirect_response=False)
        pedro = User.objects.get(username='pedro')
        self.assertTrue(pedro.groups.filter(name='Member').exists())
        self.assertTrue(AuditLog.objects.filter(username='pedro', action='register').exists())

    def test_failed_login_is_saved_in_audit_log(self):
        self.client.post(reverse('login'), {'username': 'laura', 'password': 'incorrecta'})
        self.assertTrue(AuditLog.objects.filter(username='laura', action='login_failed').exists())

    def test_display_name_without_profile(self):
        self.assertEqual(self.user.display_name(), 'laura')
        self.assertIn('avatar-h.svg', self.user.avatar_url())
