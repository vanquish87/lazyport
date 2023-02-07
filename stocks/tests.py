from django.test import TestCase
from django.test import Client
from django.urls import reverse
from unittest import mock
from stocks.views import stock_price_start, add_stock, search_list, search_stock, instrumentList
from stocks.models import Stock
from django.template.loader import render_to_string


from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware


class StockViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_add_stock(self):
        request = self.client.get(reverse('add-stock'))
        request.user = mock.Mock()
        request.user.is_authenticated = True

        response = add_stock(request)
        # Assert
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed(template_name='stocks/create-entry.html'):
            render_to_string('stocks/create-entry.html')


    def test_search_stock(self):
        request = self.client.get(reverse('search-stock'))
        request.user = mock.Mock()
        request.user.is_authenticated = True

        # Act
        response = search_stock(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'stocks/search-results.html')
        self.assertEqual(response.context_data, {})

#     # def test_search_list(self):
#     #     request = self.factory.get(reverse('search-list'))
#     #     request.user = mock.Mock()
#     #     request.user.is_authenticated = True
#     #     request.GET = {'q': 'INFY'}
#     #     mock_stock = mock.Mock()
#     #     with mock.patch('stocks.Stock.objects.filter', return_value=mock_stock):
#     #          # Act
#     #         response = search_list(request)

#     #         # Assert
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertEqual(response.template_name, 'stocks/search-list.html')
#     #         self.assertEqual(response.context_data, {'stocks': mock_stock})


#     # def test_stock_price_start(self):
#     #     request = self.factory.get(reverse('stock-price-start'))
#     #     request.user = mock.Mock()
#     #     request.user.is_authenticated = True
#     #     obj = mock.Mock()
#     #     instrument_list_response = mock.Mock()
#     #     instrument_list_response.status_code = 200
#     #     instrument_list_response.json.return_value = [
#     #         {"symbol": "INFY-EQ", "name": "Infosys Limited", "token": "INFY"}
#     #     ]
#     #     with mock.patch('requests.get', return_value=instrument_list_response):
#     #         with mock.patch('stocks.utils.loginAngel', return_value=obj):
#     #             with mock.patch('stocks.utils.records_create_update', return_value=([], [], "")):
#     #                 with mock.patch('stocks.utils.bulk_operations') as mock_bulk:
#     #                     # Annotate a request object with a session
#     #                     middleware = SessionMiddleware(lambda x: x)
#     #                     middleware.process_request(request)
#     #                     request.session.save()
#     #                     # Annotate a request object with a messages
#     #                     middleware = MessageMiddleware(lambda x: x)
#     #                     middleware.process_request(request)
#     #                     request.session.save()
#     #                     # Act
#     #                     response = stock_price_start(request)

#     #                     # Assert
#     #                     mock_bulk.assert_called_once()
#     #                     self.assertEqual(response.status_code, 302)
