from django.conf import settings
from simple_budget.helper.message import Message
from simple_budget.models.qif_parser.qif_parser import QIFParser


def quicken_import_active(request):
    """
    Is quicken import functionality turned on
    :param request:
    :return:
    """
    return {'QUICKEN_IMPORT_ACTIVE': settings.QUICKEN_IMPORT_ACTIVE}

def get_message(request):
    """
    get error/success messages for displaying to user
    :param request:
    :return: dict
    """
    message_key = request.GET.get('message', None)
    message = None
    message_type = None

    if ((not message_key or message_key == 'upload_success') and
        QIFParser.get_status() == 'in_progress'):
        message_key = 'in_progress_quicken_file'

    try:
        message = Message.MESSAGES[message_key]
        message_type = message['type']
        message = message['message']
    except KeyError:
        pass

    return {'message': message,
            'message_key': message_key,
            'message_type': message_type}
