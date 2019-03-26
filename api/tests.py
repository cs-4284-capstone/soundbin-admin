from django.test import TestCase
from django.urls import reverse

from .models import Customer


class CustomerTests(TestCase):
    def test__create(self):
        query = {"email": "admin@example.com", "walletid": "123456789"}
        self.client.post(reverse('customer-new'), data=query, content_type='application/json')
        query = Customer.objects.get(email="admin@example.com")
        print(query.to_json())
        self.assertIsNotNone(query)
