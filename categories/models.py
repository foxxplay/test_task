from __future__ import unicode_literals

import mongoengine
import datetime


class Category(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(max_length=255)
    total_sum = mongoengine.DecimalField()


class CategoriesUpload(mongoengine.Document):
    """Every upload contains information about all categories."""
    upload_dt = mongoengine.DateTimeField(default=datetime.datetime.now,
                                          help_text='Upload datetime.')
    category_column_name = mongoengine.StringField(max_length=255,
                                                   help_text='Name of column which contains categories.',
                                                   required=True)
    sum_column_name = mongoengine.StringField(max_length=255,
                                              help_text='Name of column for sum.',
                                              required=True)
    categories = mongoengine.EmbeddedDocumentListField(Category)
