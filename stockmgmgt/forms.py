from django import forms
from .models import Route, Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name', 'quantity', 'price']

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('Please enter item name')
        for instance in Stock.objects.all():
            if instance.item_name == item_name:
                raise forms.ValidationError(item_name + ' is already created')
        return item_name    

class StockSearchForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name', 'quantity', 'price']

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']


class RouteForm(forms.ModelForm):
	class Meta:
		model = Route
		fields = ['vehicle_number', 'lap_number', 'soda_200mls',  'soda_300mls',  'soda_500mls',  'soda_1000mls', 'Refreshers_350','Dasani_500mls', 'Dasani_1l', 'predator_500mls', 'power_play', 'pet_280', 'pet_350mls', 'pet_500mls', 'pet_1250mls', 'pet_2000mls', 'pet_M_Maid']  

class ExpenseForm(forms.ModelForm):
    class Meta:
        models = ['Fuel', 'Lunch', 'Car_hire']