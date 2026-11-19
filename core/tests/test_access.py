from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Broker, Qualification, User


class AccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a = Broker.objects.create(code='A', name='Corredor A')
        cls.b = Broker.objects.create(code='B', name='Corredor B')
        cls.users = {}
        for role in ('Operador', 'Consultor', 'Auditor', 'Administrador técnico'):
            group = Group.objects.create(name=role)
            user = User.objects.create_user(username=role, password='Unica-de-prueba-928!', broker=cls.a)
            user.groups.add(group)
            cls.users[role] = user
        cls.own = Qualification.objects.create(
            broker=cls.a,
            instrument='PROPIO-A',
            fiscal_year=2026,
            market='ACCIONES',
            payment_date='2026-11-18',
            sequence=10001,
            dividend_number=1,
        )
        cls.other = Qualification.objects.create(
            broker=cls.b,
            instrument='AJENO-B',
            fiscal_year=2026,
            market='ACCIONES',
            payment_date='2026-11-18',
            sequence=10001,
            dividend_number=1,
        )
        cls.official = Qualification.objects.create(
            origin='official',
            instrument='OFICIAL',
            fiscal_year=2026,
            market='ACCIONES',
            payment_date='2026-11-18',
            sequence=1,
            dividend_number=1,
        )

    def test_anonymous_cannot_open_internal_routes(self):
        for name in ('home', 'qualifications', 'entry', 'upload', 'history'):
            response = self.client.get(reverse(name))
            self.assertRedirects(response, f'/login/?next={reverse(name)}', fetch_redirect_response=False)

    def test_list_does_not_trust_broker_parameter(self):
        self.client.force_login(self.users['Operador'])
        response = self.client.get(reverse('qualifications'), {'broker': self.b.pk})
        self.assertContains(response, 'PROPIO-A')
        self.assertContains(response, 'OFICIAL')
        self.assertNotContains(response, 'AJENO-B')

    def test_direct_id_from_another_broker_is_hidden_for_every_business_role(self):
        for role in ('Operador', 'Consultor', 'Auditor'):
            self.client.force_login(self.users[role])
            self.assertEqual(
                self.client.get(reverse('qualification_detail', args=[self.other.pk])).status_code, 404
            )
            self.assertEqual(
                self.client.get(reverse('qualification_detail', args=[self.own.pk])).status_code, 200
            )

    def test_operator_routes_and_auditor_routes_are_enforced_on_server(self):
        for role in ('Consultor', 'Auditor', 'Administrador técnico'):
            self.client.force_login(self.users[role])
            for name in ('entry', 'upload'):
                self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        self.client.force_login(self.users['Operador'])
        self.assertEqual(self.client.get(reverse('entry')).status_code, 200)
        self.assertEqual(self.client.get(reverse('upload')).status_code, 200)
        self.assertEqual(self.client.get(reverse('history')).status_code, 403)
        self.client.force_login(self.users['Auditor'])
        self.assertEqual(self.client.get(reverse('history')).status_code, 200)

    def test_unassigned_and_brokerless_accounts_are_denied(self):
        for broker in (None, self.a):
            user = User.objects.create_user(username=f'no-role-{broker}', broker=broker)
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse('qualifications')).status_code, 403)
        user.groups.add(Group.objects.get(name='Operador'))
        user.broker = None
        user.save()
        self.assertEqual(self.client.get(reverse('qualifications')).status_code, 403)

    def test_inactive_broker_cannot_access_data(self):
        self.a.active = False
        self.a.save()
        self.client.force_login(self.users['Operador'])
        self.assertEqual(self.client.get(reverse('qualifications')).status_code, 403)

    def test_technical_admin_cannot_read_business_data_even_as_superuser(self):
        user = self.users['Administrador técnico']
        user.is_staff = user.is_superuser = True
        user.save()
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('qualifications')).status_code, 403)
        self.assertEqual(
            self.client.get(reverse('qualification_detail', args=[self.own.pk])).status_code, 403
        )
        self.assertEqual(self.client.get('/admin/').status_code, 200)
        self.assertEqual(self.client.get('/admin/core/qualification/').status_code, 404)

    def test_staff_flag_alone_does_not_grant_admin_access(self):
        user = self.users['Operador']
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_menu_matches_permissions(self):
        self.client.force_login(self.users['Consultor'])
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Corredor A')
        self.assertNotContains(response, f'href="{reverse("upload")}"')
        self.assertNotContains(response, f'href="{reverse("history")}"')

    def test_login_uses_hash_and_logout_clears_session(self):
        user = self.users['Operador']
        self.assertTrue(user.password.startswith('argon2$'))
        self.assertTrue(self.client.login(username=user.username, password='Unica-de-prueba-928!'))
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('home')).status_code, 302)

    def test_csrf_required_for_logout(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.users['Operador'])
        self.assertEqual(client.post(reverse('logout')).status_code, 403)

    def test_bad_login_and_external_redirect(self):
        response = self.client.post(reverse('login'), {'username': 'Operador', 'password': 'wrong'})
        self.assertContains(response, 'error', status_code=200)
        response = self.client.post(
            reverse('login') + '?next=https://example.com',
            {'username': 'Operador', 'password': 'Unica-de-prueba-928!'},
        )
        self.assertRedirects(response, reverse('home'))

    def test_placeholder_routes_cannot_write_records(self):
        self.client.force_login(self.users['Operador'])
        before = Qualification.objects.count()
        for name in ('entry', 'upload'):
            self.assertEqual(self.client.post(reverse(name), {'instrument': 'INJECTED'}).status_code, 405)
        self.assertEqual(Qualification.objects.count(), before)
