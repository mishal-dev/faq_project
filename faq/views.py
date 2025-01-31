from django.http import JsonResponse
from .models import FAQ
from django.core.cache import cache

def faq_list(request):
    lang = request.GET.get('lang', 'en')  # Default language is English
    
    faq_id = request.GET.get('id')  # Get FAQ ID from the query parameter
    if faq_id:
        # If ID is provided, fetch the FAQ with that ID
        try:
            faq = FAQ.objects.get(id=faq_id)
            # Choose language based on the query parameter
            if lang == 'hi':
                question = faq.question_hi if faq.question_hi else faq.question
                answer = faq.answer_hi if faq.answer_hi else faq.answer
            elif lang == 'bn':
                question = faq.question_bn if faq.question_bn else faq.question
                answer = faq.answer_bn if faq.answer_bn else faq.answer
            else:
                question = faq.question
                answer = faq.answer
            return JsonResponse({'question': question, 'answer': answer})
        except FAQ.DoesNotExist:
            return JsonResponse({'error': 'FAQ not found'}, status=404)
    
    # If no ID is provided, return a list of FAQs
    cached_faqs = cache.get(f'faqs_{lang}')
    if cached_faqs:
        return JsonResponse(cached_faqs, safe=False)
    
    faqs = FAQ.objects.all()
    faq_data = []

    for faq in faqs:
        if lang == 'hi':
            question = faq.question_hi if faq.question_hi else faq.question
            answer = faq.answer_hi if faq.answer_hi else faq.answer
        elif lang == 'bn':
            question = faq.question_bn if faq.question_bn else faq.question
            answer = faq.answer_bn if faq.answer_bn else faq.answer
        else:
            question = faq.question
            answer = faq.answer

        faq_data.append({
            'id': faq.id,  # Include the ID for each FAQ
            'question': question,
            'answer': answer,
        })
    
    cache.set(f'faqs_{lang}', faq_data, timeout=3600)
    return JsonResponse(faq_data, safe=False)
