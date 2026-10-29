from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from PawlyApp.models import Application, Pet
from SecurityApp.models import User


class ViewTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('luis', 'luis@example.com', 'Clave-segura-1')
        self.adopter = User.objects.create_user('ana', 'ana@example.com', 'Clave-segura-1')
        self.pet = Pet.objects.create(owner=self.owner, name='Toby', species='dog', sex='m',
                                      for_adoption=True, family='Con patio')
        self.client.login(username='ana', password='Clave-segura-1')

    def test_pages_need_login(self):
        self.client.logout()
        response = self.client.get(reverse('adoption_feed'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('adoption_feed'))

    def test_feed_shows_pets_of_other_users(self):
        Pet.objects.create(owner=self.adopter, name='Mía', species='cat', sex='f', for_adoption=True)
        response = self.client.get(reverse('adoption_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adoption_feed.html')
        self.assertContains(response, 'Toby')
        self.assertNotContains(response, 'Mía')

    def test_pet_not_found_is_404(self):
        response = self.client.get(reverse('pet_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_application_opens_chat_with_the_owner(self):
        response = self.client.post(reverse('application_form', args=[self.pet.id]), {'message': 'Quiero adoptar'})
        self.assertRedirects(response, reverse('pet_detail', args=[self.pet.id]) + '?postulacion=enviada',
                             fetch_redirect_response=False)
        application = Application.objects.get(pet=self.pet, applicant=self.adopter)
        self.assertEqual(application.chat.members.count(), 2)
        self.assertEqual(application.chat.messages.first().text, 'Quiero adoptar')

    def test_owner_cannot_apply_to_own_pet(self):
        self.client.login(username='luis', password='Clave-segura-1')
        self.client.post(reverse('application_form', args=[self.pet.id]), {'message': 'Es mía'})
        self.assertEqual(Application.objects.count(), 0)

    def test_owner_accepts_application_and_pet_changes_owner(self):
        self.client.post(reverse('application_form', args=[self.pet.id]), {'message': 'Quiero adoptar'})
        application = Application.objects.get(pet=self.pet, applicant=self.adopter)
        self.client.login(username='luis', password='Clave-segura-1')
        response = self.client.post(reverse('application_accept', args=[application.chat.id]))
        self.assertRedirects(response, reverse('chat_detail', args=[application.chat.id]), fetch_redirect_response=False)
        application.refresh_from_db()
        self.pet.refresh_from_db()
        self.assertEqual(application.status, 'accepted')
        self.assertEqual(self.pet.owner, self.adopter)
        self.assertFalse(self.pet.for_adoption)

        # Una adopción ya concretada no se puede cancelar
        self.client.login(username='ana', password='Clave-segura-1')
        self.assertEqual(self.client.post(reverse('application_cancel', args=[application.chat.id])).status_code, 404)

    def test_applicant_cannot_accept_own_application(self):
        self.client.post(reverse('application_form', args=[self.pet.id]), {'message': 'Quiero adoptar'})
        application = Application.objects.get(pet=self.pet, applicant=self.adopter)
        response = self.client.post(reverse('application_accept', args=[application.chat.id]))
        self.assertEqual(response.status_code, 404)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.owner, self.owner)

    def test_admin_panel_only_for_administrator(self):
        self.assertEqual(self.client.get(reverse('admin_panel')).status_code, 403)
        self.adopter.groups.add(Group.objects.get(name='Administrator'))
        self.assertEqual(self.client.get(reverse('admin_panel')).status_code, 200)
