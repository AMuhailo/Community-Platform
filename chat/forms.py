from django import forms
from chat.models import GroupMessage

class MessageCreateForm(forms.ModelForm):
    class  Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            "body":
                forms.TextInput(
                    attrs={
                        'placeholder':"Messages..." ,
                        'class':"w-75"
                    })
                }