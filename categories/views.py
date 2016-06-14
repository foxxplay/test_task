import xlrd
import logging
from decimal import Decimal
from collections import defaultdict
from django.views.generic import TemplateView
from django.contrib import messages
from forms import CategoryUploadForm
from exceptions import ExcelFileHandlingException
from models import Category
from models import CategoriesUpload


LOGGER = logging.getLogger('django')


class CategoriesUploadView(TemplateView):
    """Uploads *.xlsx files which contains information about categories."""
    template_name = 'upload_categories.html'
    possible_columns = [
        {
            'category_column': 'Dryden Category',
            'sum_column': 'Savings',
        },
        {
            'category_column': 'Class',
            'sum_column': 'Total Purchase Dollars'
        },
    ]

    def post(self, request, *args, **kwargs):
        """Download and handle user's excel file."""
        form = CategoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                self._save_category_information(request.FILES['excel_file'])
                messages.success(request, 'File successfully handled.')
            except ExcelFileHandlingException as e:
                messages.error(request, e.message)
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
        return self.get(request, *args, **kwargs)

    def _save_category_information(self, excel_file):
        """Search for 'category' and 'sum' columns in excel_file using 'possible_columns' list (search algorithm is
        case-sensitive) and calculate total sum for each category. Then save information into DB.
        """
        wb = xlrd.open_workbook(file_contents=excel_file.read())
        if wb.nsheets == 0:
            raise ExcelFileHandlingException('Excel file is empty.')
        sheet = wb.sheet_by_index(0)

        # Searching for columns numbers.
        headers = [cell.value for cell in sheet.row(0)][:sheet.ncols]
        for columns in self.possible_columns:
            if columns['category_column'] in headers and columns['sum_column'] in headers:

                # Calculate total sum for each category.
                result = defaultdict(Decimal)
                for category, sum_value in zip(sheet.col_values(headers.index(columns['category_column']), 1),
                                               sheet.col_values(headers.index(columns['sum_column']), 1)):
                    if category and sum_value:
                        result[category] += Decimal(sum_value)

                # Save results into DB.
                try:
                    cu = CategoriesUpload(category_column_name=columns['category_column'],
                                          sum_column_name=columns['sum_column'])
                    for category, sum_value in result.items():
                        cu.categories.append(Category(name=category, total_sum=sum_value))
                    cu.save()
                except Exception as e:
                    LOGGER.exception(e)
                    raise ExcelFileHandlingException('Database access error. Please try later.')

                break
        else:
            raise ExcelFileHandlingException('File does not contain columns for calculating.')
