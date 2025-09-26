from django.contrib import admin
from .models import Channel, Competition, Participant, Prize, PointRule

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    pass

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass

@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass

@admin.register(PointRule)
class PointRuleAdmin(admin.ModelAdmin):
    pass