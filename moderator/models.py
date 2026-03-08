from django.db import models
from django.utils import timezone


class ModRole(models.Model):

    STATUS_CHOICES = [
        ('candidate', 'Candidate'),  # earned threshold, waiting for approval
        ('active',    'Active'),     # approved by superuser
        ('revoked',   'Revoked'),    # access removed
    ]

    session_token     = models.CharField(max_length=64, unique=True)
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='candidate')
    granted_at        = models.DateTimeField(null=True, blank=True)
    revoked_at        = models.DateTimeField(null=True, blank=True)
    kindness_at_grant = models.IntegerField(default=0)

    # Log of all mod actions
    actions_today     = models.IntegerField(default=0)
    total_actions     = models.IntegerField(default=0)
    last_action_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"ModRole [{self.status}] - {self.session_token[:12]}..."

    def approve(self):
       
        self.status     = 'active'
        self.granted_at = timezone.now()
        self.save()

    def revoke(self):
        
        self.status     = 'revoked'
        self.revoked_at = timezone.now()
        self.save()

    def log_action(self):
       
        from django.utils.timezone import now
        today = now().date()

        # Reset daily counter if it's a new day
        if self.last_action_date != today:
            self.actions_today    = 0
            self.last_action_date = today

        self.actions_today += 1
        self.total_actions += 1
        self.save()

    @property
    def daily_limit_reached(self):
      
        from django.utils.timezone import now
        today = now().date()
        if self.last_action_date != today:
            return False
        return self.actions_today >= 10