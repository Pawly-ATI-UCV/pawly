from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from PawlyApp.models import Application, Pet, Profile
from SecurityApp.models import User


class ModelTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('luis', 'luis@example.com', 'Clave-segura-1')
        self.pet = Pet.objects.create(owner=self.owner, name='Toby', species='dog', sex='m',
                                      temperament='playful,calm')

    def test_pet_str_and_choices(self):
        self.assertEqual(str(self.pet), 'Toby')
        self.assertEqual(self.pet.get_species_display(), 'Perro')
        self.assertEqual(self.pet.get_sex_display(), 'Macho')

    def test_pet_age_in_years_and_months(self):
        today = date.today()
        self.pet.birth_date = date(today.year - 2, today.month, 1)
        self.assertEqual(self.pet.age(), '2 años')
        months_ago = today.month - 5 if today.month > 5 else today.month + 7
        year = today.year if today.month > 5 else today.year - 1
        self.pet.birth_date = date(year, months_ago, 1)
        self.assertEqual(self.pet.age(), '5 meses')

    def test_pet_without_birth_date_has_no_age(self):
        self.assertEqual(self.pet.age(), '')

    def test_temperament_list(self):
        self.assertEqual(self.pet.temperament_list(), 'Juguetón, Tranquilo')

    def test_pet_without_photo_uses_default_image(self):
        self.assertIn('logo-mark.png', self.pet.photo_url())

    def test_profile_name_is_used_as_display_name(self):
        Profile.objects.create(user=self.owner, full_name='Luis García', national_id='V-1')
        self.assertEqual(self.owner.display_name(), 'Luis García')

    def test_same_user_cannot_apply_twice(self):
        adopter = User.objects.create_user('ana', 'ana@example.com', 'Clave-segura-1')
        Application.objects.create(pet=self.pet, applicant=adopter, message='Hola')
        with self.assertRaises(IntegrityError):
            Application.objects.create(pet=self.pet, applicant=adopter, message='Otra vez')
