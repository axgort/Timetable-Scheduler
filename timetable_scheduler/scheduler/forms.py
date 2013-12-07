from django import forms

ALGORITHMS = [
    ('PSO', 'PSO'),
    ('Tabu', 'Tabu Search'),
    ('Genetic', 'Genetic')
]

class DataForm(forms.Form):
    algorithm = forms.ChoiceField(widget=forms.Select(), choices=ALGORITHMS)
    time = forms.IntegerField(label='Time limit')
    constraints = forms.FileField(label='File')
    #path = forms.CharField()

