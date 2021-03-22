from django.db.models import TextField
from django.forms import CharField
from django.forms import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from dynaconf import ValidationError

from applications.chat.models import Chat
from applications.chat.models import Message
from applications.profile.models import Profile


class MessengerView(TemplateView):
    template_name = "chat/messenger.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ChatCreateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()

        if not profile:
            raise ModuleNotFoundError(f"Profile {pk} not found...")

        user_profile = self.request.user.profile
        chat_pk = profile.have_chat_with(user_profile)
        if not chat_pk:
            chat = Chat.create(profile, user_profile)
            chat.save()
            chat_pk = chat.pk

        redirect_url = reverse_lazy("chat:chat", kwargs={"pk": chat_pk})

        return redirect_url


class ChatView(CreateView):
    fields = ["content"]
    model = Message
    template_name = "chat/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        pk = self.kwargs.get("pk", 0)
        chat = Chat.objects.filter(pk=pk).first()
        if not chat:
            raise FileNotFoundError(f"Chat with pk = {pk} not found...")
        context.update({"chat": chat})
        return context

    def form_valid(self, form):
        msg = form.save(commit=False)
        msg.author = self.request.user.profile

        pk = self.kwargs.get("pk", 0)
        if not pk:
            raise FileNotFoundError(f"Chat with pk = {pk} not found...")
        msg.chat_id = pk

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk", 0)
        if not pk:
            raise FileNotFoundError(f"Chat with pk = {pk} not found...")
        success_url = reverse_lazy("chat:chat", kwargs={"pk": pk})
        return success_url


class DeleteSingleMsgView(DeleteView):
    model = Message
    http_method_names = ["post"]

    def get_success_url(self):
        pk = self.kwargs.get("pk", 0)

        if not pk:
            success_url = reverse_lazy("chat:messenger")
            return success_url

        msg = Message.objects.get(pk=pk)
        success_url = reverse_lazy("chat:chat", kwargs={"pk": msg.chat_id})
        return success_url


class ChatUpdateView(View):
    def post(self, request, *args, **kwargs):

        payload = {"ok": False, "messages": [], "reason": "unknown reason"}

        chat_pk = kwargs.get("pk")
        last_message_time = kwargs.get("time")
        chat = Chat.objects.filter(pk=chat_pk).first()

        if not last_message_time:
            payload.update({"last_message_time": chat.message_set.all().last().get_datetime})

        print("chat_pk = ", chat_pk, "number = ", last_message_time)


        # if not chat:
        #     payload.update({"reason": "chat is not found"})
        #     return JsonResponse(payload)
        #
        # messages = chat.message_set.all()
        # number_of_messages = messages.count()
        #
        # if number_of_messages <= number_of_messages_on_page:
        #     payload.update({"reason": "nothing new"})
        #     return JsonResponse(payload)
        #
        # number_of_new_messages = number_of_messages - number_of_messages_on_page
        #
        # new_messages = []
        # for i in range(number_of_new_messages):
        #     new_messages.append(messages[i])
        #
        # msgs = [[message.content, message.created_at, message.author] for message in new_messages]
        #
        # payload.update(
        #     {
        #         "ok": True,
        #         "messages": msgs,
        #         "reason": None,
        #     }
        # )

        return JsonResponse(payload)
