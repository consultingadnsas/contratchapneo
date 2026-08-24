from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import CustomedContract
from .models import Contrat
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from docx import Document
import os
from unittest.mock import patch


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


class ContractDownloadIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def _create_docx_file(self, paragraphs):
        doc = Document()
        for p in paragraphs:
            doc.add_paragraph(p)

        bio = BytesIO()
        doc.save(bio)
        bio.seek(0)
        return SimpleUploadedFile('model.docx', bio.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    def test_post_without_tags_returns_docx(self):
        file = self._create_docx_file(['Bonjour', 'Ceci est un contrat sans balises.'])
        contrat = Contrat.objects.create(title='T1', description='d', prix=10.0, fichier_modele=file)

        url = reverse('contract-tags', args=[contrat.id])
        response = self.client.post(url, {'user_inputs': {}}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.wordprocessingml.document', response['Content-Type'])

    @patch('contrat.utils.convert_docx_to_pdf')
    def test_post_with_tags_returns_pdf(self, mock_convert):
        # mock conversion to avoid calling LibreOffice
        def fake_convert(docx_path, output_dir=None):
            pdf_path = os.path.join(output_dir or os.path.dirname(docx_path), os.path.splitext(os.path.basename(docx_path))[0] + '.pdf')
            with open(pdf_path, 'wb') as f:
                f.write(b'%PDF-1.4\n%fake')
            return pdf_path

        mock_convert.side_effect = fake_convert

        file = self._create_docx_file(['Bonjour {{ nom }}', 'Paragraphe'])
        contrat = Contrat.objects.create(title='T2', description='d', prix=10.0, fichier_modele=file)

        url = reverse('contract-tags', args=[contrat.id])
        response = self.client.post(url, {'user_inputs': {'nom': 'Jean'}}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/pdf', response['Content-Type'])
