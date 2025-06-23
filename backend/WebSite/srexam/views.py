from django.shortcuts import render
from .models import srexam  # Используем твою модель, предположительно sr + exam

def srexam_list(request):
    exams = srexam.objects.filter(is_public=True)
    return render(request, "srexam/srexam_list.html", {"exams": exams})