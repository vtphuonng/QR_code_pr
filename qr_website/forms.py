from django import forms
from .models import records
class ProfileImageForm(forms.Form):
    image = forms.FileField()

# Create Add Record Form
class AddRecordForm(forms.ModelForm):
	excel_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"excel_id", "class":"form-control"}), label="")
	name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"name", "class":"form-control"}), label="")
	create_day = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"create_day", "class":"form-control"}), label="")

	class Meta:
		model = records
		exclude = ("user",)