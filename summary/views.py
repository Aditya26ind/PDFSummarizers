import os
import PyPDF2
import ollama
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import PDFUploadForm
from .models import Summary

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_summary_from_ollama(text):
    try:
        prompt = f"""Please provide a well-structured summary of the following text. 
        Focus on the main points and key takeaways:
        
        {text}
        
        Provide the summary in a clear, organized format with main points and supporting details."""
        
        # Using the Ollama Python client
        response = ollama.generate(
            model='deepseek-r1:1.5b',
            prompt=prompt,
            stream=False
        )
        return response['response']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_file)
            
            # Get summary from Ollama
            summary_text = get_summary_from_ollama(text)
            # print(summary_text.split('</think>')[1])
            
            # Save to database
            summary = Summary.objects.create(
                pdf_file=pdf_file,
                summary=summary_text.split('</think>')[1]
            )
            
            return redirect('summary:result', summary_id=summary.id)
    else:
        form = PDFUploadForm()
    
    return render(request, 'upload.html', {'form': form})

def result(request, summary_id):
    summary = Summary.objects.get(id=summary_id)
    # print(summary)
    return render(request, 'result.html', {'summary': summary})