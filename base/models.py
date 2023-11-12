from django.db import models

# Create your models here.
class BaseAudit(models.Model):

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_ongoing = models.BooleanField(default=False)


class BaseAuditSection(models.Model):
    name = models.CharField(max_length=100)
    audit = models.ForeignKey(to=BaseAudit, on_delete=models.CASCADE)

class BaseAuditQuestion(models.Model):
    text = models.CharField(max_length=100)
    help = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    audit_reference = models.CharField(max_length=100)

    audit_section = models.ForeignKey(to=BaseAuditSection, on_delete=models.CASCADE)

class BaseAuditResponse(models.Model):
    text = models.CharField(max_length=100)