from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.runner import DiscoverRunner
from categories.models import CategoriesUpload
from decimal import Decimal


class NoSQLTestRunner(DiscoverRunner):
    def setup_databases(self):
        pass

    def teardown_databases(self, *args):
        pass


class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass


class TestCategories(NoSQLTestCase):
    def test_calculating(self):
        with open('SampleA.xlsx') as fp:
            resp = self.client.post(reverse('home'), {'excel_file': fp}, enctype="multipart/form-data")
        self.assertEqual(resp.status_code, 200)

        cu = list(CategoriesUpload.objects(category_column_name='Class').all()).pop()
        category = next(x for x in cu.categories if x.name == u'Non-CSP')
        self.assertEqual(category.total_sum, Decimal('233648.66'))
