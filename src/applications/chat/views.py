from django.db.models import TextField
from django.forms import CharField
from django.forms import forms
from django.http import HttpResponse
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
    template_name = "chat/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        user = self.request.user
        chat_list = user.profile.get_chat_list

        for chat in chat_list:
            chat.talker = chat.get_talker_for(user).username
            chat.save()
        return context


class ChatCreateView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()

        if not profile:
            return HttpResponse("Error! Profile not found...")

        user = self.request.user
        if profile.have_chat_with(user):
            return redirect(reverse_lazy("chat:messenger"))

        chat = Chat.create(profile.user, self.request.user)
        chat.save()
        return redirect(reverse_lazy("chat:messenger"))


class ChatView(CreateView):
    fields = ["content"]
    model = Message

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
        msg.author = self.request.user

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
        msg = Message.objects.get(pk=pk)

        success_url = reverse_lazy("chat:chat", kwargs={"pk": msg.chat_id})
        return success_url
