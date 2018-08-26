from django import forms
from . import models
from captcha.fields import ReCaptchaField

class FeedbackForm(forms.ModelForm):

    def clean_feedback_rating(self):
        data = self.cleaned_data['feedback_rating']
        if data is None:
            raise forms.ValidationError("Моля, гласувайте")
        elif data > 5:
            raise forms.ValidationError("Невалидна оценка")
        return data

    captcha = ReCaptchaField(label="Проверка за сигурност")

    class Meta:
        model = models.Feedback
        fields = ['person_name', 'feedback_text', 'feedback_rating']


class KlimatikForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_instance = self.save(commit=False)
        if model_instance.has_discount():
            self.fields['price'].help_text = "Този климатик има активно намаление, промяна в цената ще изтрие това намаление!"

    class Meta:
        model = models.Klimatik
        exclude = []