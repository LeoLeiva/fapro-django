from datetime import datetime
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from uf.tests.factories import ValuesUFFactory


class APIUFTestClass(TestCase):

    @classmethod
    def setUpTestData(self):
        self.username = "randomuser"
        self.password = "qwerty123"
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

        self.date = datetime(2022, 2, 2).date()
        self.value = Decimal('20232.32')
        self.object = ValuesUFFactory(
            date=self.date,
            value=self.value
        )

    def test_get_all_value_ok(self):
        ValuesUFFactory.create_batch(size=4)
        url = reverse('list_values_uf')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_value_from_date_ok(self):
        url = reverse('value_uf', kwargs={'value_date': self.date})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'date': '2022/02/02', 'value': '20232.32'})
        self.assertEqual(str(self.object), '2022-2-2 - 20232.32')

    def test_get_value_if_not_exist(self):
        url = reverse('value_uf', kwargs={'value_date': '2021-1-2'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content.decode(), '{"detail":"Not found."}')
