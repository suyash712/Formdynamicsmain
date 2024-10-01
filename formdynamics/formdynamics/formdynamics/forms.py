from django import forms
from grnentry.models import Grnentry1,FormData, ProcessDetails,Delivery,Supplier

class CompleteProcessForm(forms.Form):
    process_id = forms.ModelChoiceField(queryset=ProcessDetails.objects.filter(completed=False))


# forms.py
class GrnEntryForm(forms.ModelForm):
    class Meta:
        model = Grnentry1
        fields = '__all__' 
        


class FormDataForm(forms.ModelForm):
    class Meta:
        model = FormData
        fields = '__all__'

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['FINISHEDQTY', 'PDIREPORT', 'TTL_QNT_DISPATCH', 'INVOICENO', 'DELIVERYCHALLAN', 'OPTIONDC', 'BUYERNAME', 'SALESREPRESENT', 'PARTCOST','DATE']
from django import forms
from grnentry.models import material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = material
        fields = ['part_description', 'DRAW_NO', 'Material_Grade', 'Finish_size', 'Raw_material_size', 'order_size', 'DRAWING_PDF']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']