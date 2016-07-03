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
                'budget_category_add_success':
                    {'message': 'Budget category added.',
                     'type': 'success'},
                'budget_category_add_failure':
                    {'message': 'An error occurred adding a new '
                                'budget category.',
                     'type': 'danger'},
                'budget_category_edit_success':
                    {'message': 'Budget category edited.',
                     'type': 'success'},
                'budget_category_edit_failure':
                    {'message': 'An error occurred editing a '
                                'budget category.',
                     'type': 'danger'},
                'transaction_category_add_success':
                    {'message': 'Transaction category added.',
                     'type': 'success'},
                'transaction_category_add_failure':
                    {'message': 'An error occurred adding a new '
                                'transaction category.',
                     'type': 'danger'},
                'transaction_category_edit_success':
                    {'message': 'Transaction category edited.',
                     'type': 'success'},
                'transaction_category_edit_failure':
                    {'message': 'An error occurred editing a '
                                'transaction category.',
                     'type': 'danger'},
                'transaction_category_delete_success':
                    {'message': 'Transaction category deleted.',
                     'type': 'success'},
                'transaction_category_delete_failure':
                    {'message': 'An error occurred deleting a '
                                'transaction category.',
                     'type': 'danger'},
                'budget_add_success':
                    {'message': 'Budget added.',
                     'type': 'success'},
                'budget_add_failure':
                    {'message': 'An error occurred adding a budget.',
                     'type': 'danger'},
                'budget_edit_success':
                    {'message': 'Budget edited.',
                     'type': 'success'},
                'budget_edit_failure':
                    {'message': 'An error occurred editing a budget.',
                     'type': 'danger'},
                'budget_category_delete_success':
                    {'message': 'Budget category deleted.',
                     'type': 'success'},
                'budget_category_delete_failure':
                    {'message': 'An error occurred deleting a '
                                'budget category.',
                     'type': 'danger'},
                'transaction_delete_success':
                    {'message': 'Transaction deleted.',
                     'type': 'success'},
                'budget_delete_success':
                    {'message': 'Budget deleted.',
                     'type': 'success'},
                'budget_delete_failure':
                    {'message': 'An error occurred deleting the budget.',
                     'type': 'danger'},
                'budget_clone_success':
                    {'message': 'Budget cloned.',
                     'type': 'success'},
                'budget_clone_failure':
                    {'message': 'An error occurred cloning the budget.',
                     'type': 'danger'},
                'transaction_delete_failure':
                    {'message': 'An error occurred deleting a transaction.',
                     'type': 'danger'},
                'no_permissions_error':
                    {'message': 'You do no have permission to access the '
                                'requested resource.',
                     'type': 'danger'},
                'logged_out':
                    {'message': 'You have logged out.',
                     'type': 'success'},
                'in_progress_quicken_file':
                    {'message': 'Quicken QIF file processing.',
                     'type': 'success'}}


