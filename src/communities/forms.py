from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from communities.models import Community,Member
#from django_bootstrap_wysiwyg.widgets import WysiwygInput

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        exclude=('slug','created_by','site','blocked')
        """
        widgets = {
            'description': WysiwygInput()
        }
        """

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.form_class = 'form-horizontal'
        super(CommunityForm, self).__init__(*args, **kwargs)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields=('accepted','member_type','blocked')
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.form_class = 'form-horizontal'
        super(MemberForm, self).__init__(*args, **kwargs)
