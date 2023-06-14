import datetime
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form) :
    renewal_date=forms.DateField(help_text="Enter a date btw now and 4 weeks (def is 3).")
    
    def clean_renewal_date(self) :
        data= self.cleaned_data['renewal_date']
        
        "checking for the range"
        if data < datetime.date.today() :
            raise ValidationError(_("invalid input! Past date detected"))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4) :
            raise ValidationError(_("Invalid inpur! Extended date detected"))
        
        return data 
from .models import BookInstance    
class RenewBookModelForm(forms.ModelForm) :
    class Meta :
        model = BookInstance
        fields = ['due_back']
        labels={"due_back":_('New Date')}
        help_texts={"due_back":_("Enter Date btw now and 4 weeks (e.g 2020/05/24), (dep 3)")}
        
    def clean_due_back(self):
        data=self.cleaned_data['due_back']
        
        '''checking the range of the date '''
        if data < datetime.date.today() :
            raise ValidationError(_("past date detection"))
        if data > datetime.date.today() + datetime.timedelta(weeks=4) :
            raise ValidationError(_("Extended date detection"))
        return data
             