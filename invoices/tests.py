from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail
from django.urls import reverse

# Create your tests here.
class InvoiceAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def create_invoice(self, customer_name, invoice_details=[]):
        invoice = Invoice.objects.create(customer_name=customer_name)

        for detail_data in invoice_details:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        return invoice

    def test_create_invoice(self):
        data = {'customer_name': 'Test Customer'}
        response = self.client.post(reverse('invoice-list'), data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().customer_name, 'Test Customer')
    
    def test_create_invoice_with_details(self):
        data = {
            'customer_name': 'Test Customer',
            'invoice_details': [
                {'description': 'Item 1', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Item 2', 'quantity': 3, 'unit_price': 15.0},
            ]
        }

        response = self.client.post(reverse('invoice-list'), data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        invoice = Invoice.objects.get(pk=response.data['invoice_number'])
        print(invoice.invoice_number, invoice.customer_name, invoice.date, invoice.invoice_details.all())
        self.assertEqual(invoice.invoice_details.count(), 2)
        
        for detail in invoice.invoice_details.all():
            self.assertEqual(detail.price, detail.quantity * detail.unit_price)
    
    def test_retrieve_invoice(self):
        invoice = self.create_invoice(customer_name='Test Customer')
        response = self.client.get(reverse('invoice-detail', args=[invoice.invoice_number]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')
    
    def test_retrieve_invoice_with_details(self):
        invoice = self.create_invoice(customer_name='Test Customer', invoice_details=[
            {'description': 'Item 1', 'quantity': 2, 'unit_price': 10.0},
            {'description': 'Item 2', 'quantity': 3, 'unit_price': 15.0},
        ])

        response = self.client.get(reverse('invoice-detail', args=[invoice.invoice_number]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.data['customer_name'], len(response.data['invoice_details']))

        self.assertEqual(response.data['customer_name'], 'Test Customer')
        self.assertEqual(len(response.data['invoice_details']), 2)

    def test_update_invoice(self):
        invoice = self.create_invoice(customer_name='Test Customer')
        data = {'customer_name': 'Updated Customer'}
        response = self.client.put(reverse('invoice-detail', args=[invoice.invoice_number]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get().customer_name, 'Updated Customer')
    
    def test_update_invoice_with_details(self):
        invoice = self.create_invoice(customer_name='Test Customer')

        data = {
            'customer_name': 'Updated Customer',
            'invoice_details': [
                {'description': 'Updated Item 1', 'quantity': 1, 'unit_price': 5.0},
                {'description': 'New Item', 'quantity': 4, 'unit_price': 20.0},
            ]
        }

        response = self.client.put(reverse('invoice-detail', args=[invoice.invoice_number]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invoice.refresh_from_db()
        self.assertEqual(invoice.customer_name, 'Updated Customer')
        self.assertEqual(invoice.invoice_details.count(), 2)

    def test_delete_invoice(self):
        invoice = self.create_invoice(customer_name='Test Customer')
        response = self.client.delete(reverse('invoice-detail', args=[invoice.invoice_number]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)