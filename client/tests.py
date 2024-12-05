from datetime import timedelta
from django.utils import timezone  # Importa directamente timezone para usar timezone.now()
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from client.models import Client


class ClientListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(12):
            Client.objects.create(
                name=f"Client {i}",
                dni=f"12345678{i:02d}",  
                celphone=f"555-555-{i:03d}",
                address=f"Address {i}",
                observation=f"Observation for client {i}",
                active_membership=(i % 2 == 0),
                active_until=(timezone.now().date() if i % 2 == 0 else None),
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('client_list'))  
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('client_list'))
        self.assertTemplateUsed(response, 'client/all.html')

    def test_pagination_is_six(self):
        response = self.client.get(reverse('client_list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['clients']), 6)

    def test_lists_all_clients(self):
        # Verificar la segunda página de la paginación
        response = self.client.get(reverse('client_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['clients']), 6)


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_client = Client.objects.create(
            name="Active Client",
            dni="1234567890",
            celphone="555-555-0001",
            address="Active Address",
            active_membership=True,
            active_until=timezone.now().date() + timedelta(days=30),
        )
        cls.inactive_client = Client.objects.create(
            name="Inactive Client",
            dni="1234567891",
            celphone="555-555-0002",
            address="Inactive Address",
            active_membership=True,
            active_until=timezone.now().date() - timedelta(days=1),
        )

    def test_is_membership_active_for_active_client(self):
        self.assertTrue(self.active_client.is_membership_active())

    def test_is_membership_active_for_inactive_client(self):
        self.assertFalse(self.inactive_client.is_membership_active())

    def test_is_membership_active_when_no_active_until(self):
        client = Client.objects.create(
            name="No Date Client",
            dni="1234567892",
            celphone="555-555-0003",
            address="No Date Address",
            active_membership=True,
            active_until=None,
        )
        self.assertFalse(client.is_membership_active())

    def test_is_membership_active_when_not_active(self):
        client = Client.objects.create(
            name="Inactive Membership",
            dni="1234567893",
            celphone="555-555-0004",
            address="Inactive Membership Address",
            active_membership=False,
            active_until=timezone.now().date() + timedelta(days=30),
        )
        self.assertFalse(client.is_membership_active())
    
    def test_client_image_upload(self):
        client = Client.objects.create(
            name="Client with Image",
            dni="1234567894",
            celphone="555-555-0005",
            address="Image Address",
            image="path/to/image.jpg",
        )
        self.assertEqual(client.image.name, "path/to/image.jpg")

    def test_client_without_image(self):
        client = Client.objects.create(
            name="Client without Image",
            dni="1234567895",
            celphone="555-555-0006",
            address="No Image Address",
        )
    
        self.assertTrue(client.image.name == None)


class ClientDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_instance = Client.objects.create(
            name="Client Detail Test",
            dni="1234567890",
            celphone="555-555-0001",
            address="Address Test",
        )
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/clients/{self.client_instance.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('client_detail', kwargs={'pk': self.client_instance.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_uses_correct_template(self):
        response = self.client.get(reverse('client_detail', kwargs={'pk': self.client_instance.pk}))
        self.assertTemplateUsed(response, 'client/detail.html')
    
    def test_context_data(self):
        response = self.client.get(reverse('client_detail', kwargs={'pk': self.client_instance.pk}))
        self.assertEqual(response.context['client'], self.client_instance)


class CreateClientViewTest(TestCase):
    def test_create_client_post_valid_data(self):
        data = {
            'name': 'New Client',
            'dni': '1234567899',
            'celphone': '555-555-1000',
            'address': 'New Address',
        }
        response = self.client.post(reverse('client_add'), data)
        self.assertRedirects(response, reverse('client_list'))
        self.assertEqual(Client.objects.count(), 1)
    
    def test_create_client_post_invalid_data(self):
        data = {
            'name': '',  # Missing name to trigger form validation error
            'dni': '1234567899',
            'celphone': '555-555-1000',
            'address': 'New Address',
        }
        response = self.client.post(reverse('client_add'), data)
        self.assertEqual(response.status_code, 200)  # Ensure it returns to the form
        self.assertFormError(response.context['form'], 'name', 'Este campo es obligatorio.')
    
    def test_create_client_get(self):
        response = self.client.get(reverse('client_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/add.html')


class UpdateClientViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_instance = Client.objects.create(
            name="Client to Update",
            dni="1234567890",
            celphone="555-555-0001",
            address="Address Test",
        )

    def test_update_client_post_valid_data(self):
        data = {
            'name': 'Updated Client',
            'dni': '1234567890',
            'celphone': '555-555-2000',
            'address': 'Updated Address',
        }
        response = self.client.post(reverse('client_update', kwargs={'pk': self.client_instance.pk}), data)
        self.assertRedirects(response, reverse('client_list'))
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.name, 'Updated Client')

    def test_update_client_post_invalid_data(self):
        data = {
            'name': '',  # Missing name to trigger form validation error
            'dni': '1234567890',
            'celphone': '555-555-2000',
            'address': 'Updated Address',
        }
        response = self.client.post(reverse('client_update', kwargs={'pk': self.client_instance.pk}), data)
        self.assertEqual(response.status_code, 200)  # Ensure it returns to the form
        self.assertFormError(response.context['form'], 'name', 'Este campo es obligatorio.')

    def test_update_client_get(self):
        response = self.client.get(reverse('client_update', kwargs={'pk': self.client_instance.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/update.html')
        self.assertEqual(response.context['client'], self.client_instance)


class ClientDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_instance  = Client.objects.create(
            name="Client to Delete",
            dni="1234567890",
            celphone="555-555-0001",
            address="Address Test",
        )

    def test_delete_client_post(self):
        response = self.client.post(reverse('client_delete', kwargs={'pk': self.client_instance.pk}))
        self.assertRedirects(response, reverse('client_list'))
        self.assertEqual(Client.objects.count(), 0)

    def test_delete_client_get(self):
        response = self.client.get(reverse('client_delete', kwargs={'pk': self.client_instance.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/delete.html')

class ListClientByKeywordTest(TestCase):

    def setUp(self):
        self.client1 = Client.objects.create(name="John Doe", dni="1234567890", celphone="555-555-1000", address="Address 1")
        self.client2 = Client.objects.create(name="Jane Smith", dni="0987654321", celphone="555-555-2000", address="Address 2")
    
    def test_search_clients_by_name(self):
        response = self.client.get(reverse('client_search') + '?' + urlencode({'kword': 'John'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['clients'],
            [self.client1]
        )
    
    def test_search_clients_by_dni(self):
        response = self.client.get(reverse('client_search') + '?' + urlencode({'kword': '0987654321'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['clients'],
            [self.client2]
        )
    
    def test_search_no_results(self):
        response = self.client.get(reverse('client_search') + '?' + urlencode({'kword': 'Nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['clients'],
            []
        )
    
    def test_search_empty_keyword(self):
        response = self.client.get(reverse('client_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['clients'],
            []
        )
