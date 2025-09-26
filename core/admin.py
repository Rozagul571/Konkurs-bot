from django.contrib import admin
from .models import Channel, Competition, Participant, Prize, PointRule

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_username', 'title', 'type', 'competition')
    list_filter = ('type', 'competition')
    search_fields = ('channel_username', 'title')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'admin')
    list_filter = ('status',)
    search_fields = ('title',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'total_points', 'is_active')
    list_filter = ('is_active', 'competition')
    search_fields = ('user__username', 'user__full_name')

@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('competition', 'place', 'prize_name', 'prize_amount')
    list_filter = ('competition', 'place')
    search_fields = ('prize_name',)

@admin.register(PointRule)
class PointRuleAdmin(admin.ModelAdmin):
    pass