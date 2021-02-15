from django.http import HttpRequest


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Update talker name for user
        if request.path.startswith("/messenger") and request.method.lower() == "get":
            profile = request.user.profile
            chats = profile.chat_set.all()

            for chat in chats:
                chat.talker = chat.get_talker_for(profile)
                chat.save()

        response = self.get_response(request)

        return response
