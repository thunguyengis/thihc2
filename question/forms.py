from django import forms
from .models import *
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class QuestionForm(forms.Form):
  
    question_content = forms.CharField(widget=CKEditorUploadingWidget())
                    

   