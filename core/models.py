from django.db import models
from django.utils import timezone
import uuid

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CompetitionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    FINISHED = "finished", "Finished"

class PointAction(models.TextChoices):
    REFERRAL = "referral", "Referral"
    CHANNEL_JOIN = "channel_join", "Join All Channels"
    PREMIUM_REFERRAL = "premium_referral", "Premium Referral"
    TASK_INSTAGRAM = "task_instagram", "Instagram Task"

class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    PARTICIPANT = "participant", "Participant"
    PREMIUM = "premium", "Premium"

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.PARTICIPANT)
    joined_at = models.DateTimeField(default=timezone.now)
    referral_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username or str(self.telegram_id)


class Participant(models.Model):
    total_points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)

    def update_points(self, action_type, rule):
        if action_type == PointAction.REFERRAL:
            referral = Referral.objects.filter(referrer=self.user, competition=self.competition).first()
            if referral and referral.referred.is_premium:
                points = rule.points * rule.prem_ball
            else:
                points = rule.points
        elif action_type == PointAction.CHANNEL_JOIN:
            points = rule.points * (rule.prem_ball if self.user.is_premium else 1)
        else:
            points = rule.points

        self.total_points += points
        self.save()
        Point.objects.create(participant=self, points=points, reason=action_type)

    class Meta:
        unique_together = ('user', 'competition')

    def __str__(self):
        return f"{self.user} in {self.competition}"


class Channel(TimestampMixin):
    class ChannelType(models.TextChoices):
        CHANNEL = 'channel', 'Channel'
        GROUP = 'group', 'Group'

    channel_username = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=20, choices=ChannelType.choices, default=ChannelType.CHANNEL)

    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='channels')

    class Meta:
        db_table = 'channels'

    def __str__(self):
        return self.channel_username or self.title

class Competition(TimestampMixin):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CompetitionStatus.choices, default=CompetitionStatus.ACTIVE)

    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_competitions", null=True)
    # total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class PointRule(models.Model):
    action_type = models.CharField(max_length=50, choices=PointAction.choices, default=PointAction.REFERRAL)
    points = models.IntegerField(default=0)
    prem_ball = models.FloatField(default=1.0, help_text="Premium")
    start_time = models.DateTimeField(null=True, blank=True)

    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('competition', 'action_type')

    def __str__(self):
        return f"{self.get_action_type_display()} ({self.points} ball)"

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invited_by")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="referrals")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("referrer", "referred", "competition")

    def __str__(self):
        return f"{self.referred} <- {self.referrer}"



class Prize(models.Model):
    place = models.PositiveIntegerField()
    prize_name = models.CharField(max_length=200, null=True, blank=True)
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="prizes")

    class Meta:
        unique_together = ("competition", "place")

    def __str__(self):
        return f"{self.competition} - {self.place}th Prize ({self.prize_name})"

class Point(models.Model):
    points = models.IntegerField()
    reason = models.CharField(max_length=50, choices=PointAction.choices)
    created_at = models.DateTimeField(default=timezone.now)

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="points")

    def __str__(self):
        return f"{self.participant.user} earned {self.points} for {self.reason}"