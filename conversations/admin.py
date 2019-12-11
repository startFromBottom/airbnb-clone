from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definitions """

    list_display = ("__str__", "created")

    pass


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definitions """

    list_display = ("__str__", "count_messages", "count_participants")

    pass
