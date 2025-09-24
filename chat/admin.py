from django.contrib import admin
from .models import User, Admin, Competition, Channel, Prize, Participant, Referral, Point, Winner, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    pass

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass