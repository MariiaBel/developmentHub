def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Не заполнено обязательное поле.',
            params={'value': value},
        ) 