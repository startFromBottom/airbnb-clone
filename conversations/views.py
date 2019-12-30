from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import DetailView
from users import models as user_models
from . import models, forms


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get(pk=a_pk)  # get_or_none : not recognized
    user_two = user_models.User.objects.get(pk=b_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))

        print(conversation)


class ConversationDetailView(DetailView):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        # form = forms.AddCommentForm
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {
                "conversation": conversation,
                # "form": form,
            },
        )

    def post(self, *args, **kwargs):
        # form = forms.AddCommentForm(self.request.POST)
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
