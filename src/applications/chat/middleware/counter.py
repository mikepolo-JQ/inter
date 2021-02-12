from django.http import HttpRequest


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Update talker name for user
        if request.path.startswith("/messenger") and request.method.lower() == "get":
            profile = request.user.profile
            chat_list = profile.get_chat_list

            for chat in chat_list:
                chat.talker = chat.get_talker_for(profile)
                chat.save()

        response = self.get_response(request)

        return response
