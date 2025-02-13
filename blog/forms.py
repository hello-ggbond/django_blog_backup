from django import forms


class BlogPubForm(forms.Form):
    title = forms.CharField(max_length=120, min_length=2)
    content = forms.CharField(min_length=2, error_messages={'required':'What Fucking!!!'})
    category = forms.IntegerField()
