from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'Super Admin'
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class User(AbstractUser, TimestampMixin):
    telegram_id = models.BigIntegerField(unique=True)
    is_premium = models.BooleanField(default=False)
    username = models.CharField(max_length=56, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    REQUIRED_FIELDS = ["telegram_id"]

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username or self.first_name}"

class Admin(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Competition(TimestampMixin):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        FINISHED = 'finished', 'Finished'

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='created_competitions')

    class Meta:
        db_table = 'competitions'

    def __str__(self):
        return self.title

class Channel(TimestampMixin):
    class ChannelType(models.TextChoices):
        CHANNEL = 'channel', 'Channel'
        GROUP = 'group', 'Group'

    channel_username = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=20, choices=ChannelType.choices, default=ChannelType.CHANNEL)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='channels')

    class Meta:
        db_table = 'channels'

    def __str__(self):
        return self.channel_username

class Prize(TimestampMixin):
    place = models.IntegerField()
    prize_name = models.CharField(max_length=200, null=True, blank=True)
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='prizes')

    class Meta:
        db_table = 'prizes'

    def __str__(self):
        return f"{self.prize_name} (Place {self.place})"

class Participant(TimestampMixin):
    referral_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    total_points = models.IntegerField(default=0)
    referrals_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participants')

    class Meta:
        db_table = 'participants'
        unique_together = ('user', 'competition')

    def __str__(self):
        return f"{self.user.username} in {self.competition.title}"

class Referral(TimestampMixin):
    referrer = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='referred_by')

    class Meta:
        db_table = 'referrals'

    def __str__(self):
        return f"{self.referrer} referred {self.referred}"

class Point(TimestampMixin):
    class EventType(models.TextChoices):
        REFERRAL = 'referral', 'Referral'
        TASK_COMPLETION = 'task_completion', 'Task Completion'
        BONUS = 'bonus', 'Bonus'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='points')
    points = models.PositiveIntegerField()
    event_type = models.CharField(max_length=30, choices=EventType.choices, default=EventType.REFERRAL)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'points'

    def __str__(self):
        return f"{self.event_type}: {self.points} points"

class Winner(TimestampMixin):
    place = models.IntegerField()
    awarded_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_proof_url = models.CharField(max_length=300, null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='winners')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='wins')

    class Meta:
        db_table = 'winners'

    def __str__(self):
        return f"Winner {self.participant.user.username} (Place {self.place})"

class Payment(TimestampMixin):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    winner = models.ForeignKey(Winner, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    method = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    receipt_url = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment {self.amount} ({self.status})"