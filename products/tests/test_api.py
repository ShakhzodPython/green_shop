from rest_framework.test import APITestCase

# Проверка категорий товаров на GET запрос
class ProductsCategoryAPITestCase(APITestCase):
    def test_get(self):
        url = 'http://127.0.0.1:8000/api/products/category/'
        response = self.client.get(url)
        print(response.data)
