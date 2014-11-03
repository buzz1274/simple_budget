class Message(object):

    messages = {'upload_success':
                    {'message': 'Quicken QIF successfully uploaded.',
                     'type': 'success'},
                'quicken_upload_complete':
                    {'message': 'Quicken QIF successfully processed.',
                     'type': 'success'},
                'quicken_upload_failed':
                    {'message': 'An error occurred processing Quicken QIF file.',
                     'type': 'danger'},
                'in_progress_quicken_file':
                    {'message': 'Quicken QIF file processing.',
                     'type': 'success'}}

    def get_message(self, message_key):
        """
        returns message and type
        :return:
        """
        try:
            message = self.messages[message_key]
            return [message_key, message['message'], message['type']]
        except KeyError:
            return [False, False, False]
