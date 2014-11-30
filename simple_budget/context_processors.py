from django.conf import settings
from simple_budget.helper.message import Message
from simple_budget.models.transaction.qif_parser import QIFParser
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory


def quicken_import_active(request):
    """
    Is quicken import functionality turned on
    :param request:
    :return:
    """
    return {'QUICKEN_IMPORT_ACTIVE': settings.QUICKEN_IMPORT_ACTIVE}

def unassigned_transaction_categories(request):
    """
    display a message if a transaction category is not assigned to a
    budget category
    :param request:
    :return:
    """
    unassigned_transaction_categories = \
        TransactionCategory.objects.filter(budget_category=None).count()

    return {"unassigned_transaction_categories":
                unassigned_transaction_categories}

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
