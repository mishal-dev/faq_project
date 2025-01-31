from django.contrib import admin
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    # Exclude the language-specific fields from the form
    exclude = ('question_hi', 'answer_hi', 'question_bn', 'answer_bn')
    
    # Optionally, you can display the translations in the list view or the read-only fields in the form
    list_display = ('question', 'answer','question_hi',  'answer_hi', 'question_bn', 'answer_bn')

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to handle translation generation when saving.
        """
        # Generate translations for Hindi and Bengali when saving.
        obj.save()  # This will trigger the translation in the model's `save()` method.
        super().save_model(request, obj, form, change)

# Register the FAQ model with the custom admin
admin.site.register(FAQ, FAQAdmin)
