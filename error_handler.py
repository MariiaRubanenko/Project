# class ErrorHandler:
#     @staticmethod
#     def handle_error(exception, message="An error occurred"):
#         # Логирование ошибки можно добавить здесь
#         # Например, logging.error(exception)
#
#         # Возврат ответа с ошибкой
#         return {
#             'success': False,
#             'message': f"{message}: {str(exception)}"
#         }, 500
#
#     @staticmethod
#     def handle_validation_error(message):
#         return {
#             'success': False,
#             'message': message
#         }, 400

class ErrorHandler:
    @staticmethod
    def handle_error(exception, message="An error occurred"):
        return {
            'success': False,
            'message': f"{message}: {str(exception)}"
        }, 500

    @staticmethod
    def handle_validation_error(message):
        # Если message — это объект, Marshmallow может передать словарь ошибок
        if isinstance(message, dict):
            # Преобразуем словарь ошибок в строку для удобного отображения
            error_messages = []
            for field, errors in message.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            message = "; ".join(error_messages)

        return {
            'success': False,
            'message': message
        }, 400
