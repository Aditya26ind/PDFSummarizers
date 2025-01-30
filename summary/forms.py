from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        label='Select a PDF file',
        help_text='Max file size: 5MB',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )