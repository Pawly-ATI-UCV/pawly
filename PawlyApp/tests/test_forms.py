from django.test import TestCase

from PawlyApp.forms import ApplicationForm, MessageForm, PetForm, ProfileForm


class FormTests(TestCase):

    def test_pet_form_valid(self):
        form = PetForm({'name': 'Mía', 'species': 'dog', 'sex': 'f'})
        self.assertTrue(form.is_valid())

    def test_pet_form_needs_name(self):
        form = PetForm({'name': '', 'species': 'dog', 'sex': 'f'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_pet_for_adoption_needs_family(self):
        # Para ponerla en adopción hay que llenar las características buscadas
        form = PetForm({'name': 'Mía', 'species': 'dog', 'sex': 'f', 'for_adoption': 'on', 'family': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('family', form.errors)

        form = PetForm({'name': 'Mía', 'species': 'dog', 'sex': 'f', 'for_adoption': 'on', 'family': 'Con patio'})
        self.assertTrue(form.is_valid())

    def test_application_form_needs_message(self):
        self.assertFalse(ApplicationForm({'message': '   '}).is_valid())
        self.assertTrue(ApplicationForm({'message': 'Quiero adoptar'}).is_valid())

    def test_profile_form_needs_name_and_national_id(self):
        form = ProfileForm({'full_name': '', 'national_id': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('national_id', form.errors)

    def test_message_form_needs_text(self):
        self.assertFalse(MessageForm({'text': ''}).is_valid())
        self.assertTrue(MessageForm({'text': 'Hola'}).is_valid())
