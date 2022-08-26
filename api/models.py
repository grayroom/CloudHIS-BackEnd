from django.db import models


class Template(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    parent_id = models.ForeignKey(
        "Template", on_delete=models.CASCADE, null=True, blank=True, db_column="parent_id")

    is_directory = models.BooleanField(default=False)
    file_name = models.CharField(max_length=50)
    file_content = models.JSONField(default='{}')

    created_time = models.DateTimeField(auto_now_add=True)
