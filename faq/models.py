from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    # Language-specific translations (These fields won't be shown in the admin form)
    question_hi = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate Hindi and Bengali translations
        for question and answer when an FAQ is created or updated.
        If translation fails, fallback to English.
        """
        translator = Translator()

        # Translate to Hindi and Bengali if not already provided
        if not self.question_hi or not self.answer_hi:
            try:
                if not self.question_hi:
                    self.question_hi = translator.translate(self.question, src='en', dest='hi').text
                if not self.answer_hi:
                    self.answer_hi = translator.translate(self.answer, src='en', dest='hi').text
            except Exception as e:
                # Log the error and fall back to English
                self.question_hi = self.question
                self.answer_hi = self.answer
                print(f"Error in translation (Hindi): {e}")

        if not self.question_bn or not self.answer_bn:
            try:
                if not self.question_bn:
                    self.question_bn = translator.translate(self.question, src='en', dest='bn').text
                if not self.answer_bn:
                    self.answer_bn = translator.translate(self.answer, src='en', dest='bn').text
            except Exception as e:
                # Log the error and fall back to English
                self.question_bn = self.question
                self.answer_bn = self.answer
                print(f"Error in translation (Bengali): {e}")

        super(FAQ, self).save(*args, **kwargs)

    def __str__(self):
        return self.question[:50]  # Display only the first 50 characters in admin
