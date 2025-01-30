from django.db import models

class Summary(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary {self.id} - {self.created_at}"