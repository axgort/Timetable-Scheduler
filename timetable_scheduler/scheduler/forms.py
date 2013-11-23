from django import forms

ALGORITHMS = [
    ('PSO', 'PSO'),
    ('Tabu Search', 'Tabu Search'),
    ('Genetic', 'Genetic')
]

class DataForm(forms.Form):
    algorithm = forms.ChoiceField(widget=forms.Select(), choices=ALGORITHMS)
    time = forms.IntegerField(label='Time limit')
    #path = forms.FilePathField()
    path = forms.CharField()
