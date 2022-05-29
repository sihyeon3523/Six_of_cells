from django import forms
from .models import UserName

class PostForm(forms.ModelForm):
    class Meta:
        model = UserName
        fields=("name",)
