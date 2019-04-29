from django.forms import ModelForm 

def get_form_class(model, base=ModelForm):
    model_ = model

    class Meta:
        model = model_
        fields = '__all__'

    attrs = dict(
        Meta = Meta,
        )
    return type(str(model_.__name__ + 'Form'), (base, ), attrs )