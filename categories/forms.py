import os
from django import forms


ALLOWED_UPLOAD_FILE_TYPES = (
    '.xlsx',
)


class CategoryUploadForm(forms.Form):
    excel_file = forms.FileField(required=True, label='Excel file', error_messages={'required': "File is required."})

    def clean_excel_file(self):
        """Checking for file type."""
        excel_file = self.cleaned_data['excel_file']
        file_type = os.path.splitext(excel_file.name)[1]
        if file_type not in ('.xlsx', ):
            raise forms.ValidationError('Incorrect file type.')
        return excel_file
