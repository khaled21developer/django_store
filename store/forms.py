from django import forms
from .models import SupportRequest
from django.contrib.auth.models import User

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'message']

class EmailForm(forms.Form):
    subject = forms.CharField(label="الموضوع", max_length=100)
    message = forms.CharField(label="المحتوى", widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(
        label="المستخدمين",
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '10'})
    )
    # إضافة حقل للمرفقات (اختياري)
    # attachment = forms.FileField(label="المرفق", required=False)