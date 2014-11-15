class Message(object):

    MESSAGES = {'upload_success':
                    {'message': 'Quicken QIF successfully uploaded.',
                     'type': 'success'},
                'quicken_upload_complete':
                    {'message': 'Quicken QIF successfully processed.',
                     'type': 'success'},
                'quicken_upload_failed':
                    {'message': 'An error occurred processing Quicken QIF file.',
                     'type': 'danger'},
                'transaction_edit_success':
                    {'message': 'Transaction edited.',
                     'type': 'success'},
                'transaction_edit_failure':
                    {'message': 'An error occurred editing the transaction.',
                     'type': 'danger'},
                'transaction_add_success':
                    {'message': 'Transaction added.',
                     'type': 'success'},
                'transaction_add_failure':
                    {'message': 'An error occurred adding a new transaction.',
                     'type': 'danger'},
                'transaction_delete_success':
                    {'message': 'Transaction deleted.',
                     'type': 'success'},
                'transaction_delete_failure':
                    {'message': 'An error occurred deleting a transaction.',
                     'type': 'danger'},
                'in_progress_quicken_file':
                    {'message': 'Quicken QIF file processing.',
                     'type': 'success'}}


