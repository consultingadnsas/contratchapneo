from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import CustomedContract


class CustomContractRequestViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('custom-contract-requests')

    def test_create_custom_contract_request(self):
        payload = {
            'subject': 'Contrat de partenariat',
            'phone_number': '770000001',
            'email': 'client@example.com',
            'description': 'Besoin d’un contrat sur mesure pour un partenariat commercial.',
            'price': 50000.0,
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomedContract.objects.count(), 1)
        self.assertEqual(CustomedContract.objects.get().subject, payload['subject'])
        self.assertEqual(CustomedContract.objects.get().email, payload['email'])
