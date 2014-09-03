from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import os
import subprocess


class Transaction(models.Model):
    """
    transaction model
    """
    transaction_id = models.IntegerField(primary_key=True)
    transaction_date = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'transaction'

    @staticmethod
    def process_upload_quicken_file(quicken_file):
        """
        saves and process the uploaded quicken file
        :param quicken_file:
        :return: boolean
        """
        filename = settings.TEMP_SAVE_PATH + quicken_file.name.lower()

        try:
            os.remove(filename)
        except OSError:
            pass

        with open(filename, 'w+') as destination:
            for chunk in quicken_file.chunks():
                destination.write(chunk)

        if not os.path.isfile(filename):
            return False
        else:
            subprocess.call(['python',
                             '%s/scripts/qif_file_parser.py' % (settings.BASE_DIR,),
                             filename])
            return True
