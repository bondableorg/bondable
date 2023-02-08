from django.db import models

# Create your models here.
class ReportEngine(BaseModel, models.Model):
    id = HashedAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    type = models.CharField(
        choices=(("metabase", "Metabase"),), default="metabase", max_length=50
    )
    base_url = models.URLField()
    integration_api_key = models.CharField(max_length=250)

class EmbeddedReport(BaseModel, models.Model):
    id = HashedAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    engine = models.ForeignKey(ReportEngine, on_delete=models.PROTECT)
    reference_id = models.CharField(
        help_text="Report ID on the engine, like question id, dashboard id on Metabase",
        max_length=50,
    )
    reference_type = models.CharField(
        choices=(
            ("single_report", "Question/Single Report"),
            ("dashboard", "Dashboard"),
        ),
        max_length=50,
    )
    active = models.BooleanField(default=False)