import pytest
from django.urls import reverse
from rest_framework import status
from .models import FAQ

@pytest.mark.django_db
def test_faq_translation():
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    faq.translate()
    
    assert faq.question_hi is not None
    assert faq.question_bn is not None

@pytest.mark.django_db
def test_api_faqs():
    url = reverse('faq_list')
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
