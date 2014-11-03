from django.db import models


class QIFParser(models.Model):
    """
    budget type model
    """
    parse_status = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'qif_parser'


    @staticmethod
    def get_status():
        """
        gets status for last uploaded qif file
        :return:
        """
        try:
            parsed_quicken_file_status = QIFParser.objects.all().order_by('-id')[:1]

            if parsed_quicken_file_status:
                return parsed_quicken_file_status[0].parse_status
            else:
                return False
        except IndexError:
            return False