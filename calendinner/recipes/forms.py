from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeStep, Ingredient, UnitMeasure, IngredientQuantity, Tag
from django.urls import reverse_lazy

class RecipeForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Quantity")
    unit_measure = forms.ModelChoiceField(queryset=UnitMeasure.objects.all(), label="Unit of Measure")
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time', 'serving_size', 'user', 'image_filename', 'tags', 'ingredients', 'quantity', 'unit_measure', 'steps']
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'prep_time': forms.NumberInput(),
            'cook_time': forms.NumberInput(),
            'serving_size': forms.NumberInput(),
            'user': forms.HiddenInput(),
            'image_filename': forms.TextInput(),
            'tags': forms.CheckboxSelectMultiple(),
            'ingredients': forms.TextInput(),
            'steps': forms.TextInput()
        }

ingredient_formset = inlineformset_factory(Recipe, IngredientQuantity, fields=['ingredient', 'quantity', 'unit_measure'], extra=1, can_delete=False)
recipe_step_formset = inlineformset_factory(Recipe, RecipeStep, fields=['recipe_step'], extra=1, can_delete=False)

      
class RecipeStepForm(forms.ModelForm):
    step = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter step details here...'}), label="Step Details", )
    
    class Meta:
      model = RecipeStep
      fields = ['step']

class IngredientQuantityForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Quantity")
    unit_measure = forms.ModelChoiceField(queryset=UnitMeasure.objects.all(), label="Unit of Measure")

    class Meta:
        model = IngredientQuantity
        fields = ['quantity', 'unit_measure']

class IngredientForm(forms.ModelForm):
    ingredient_name = forms.CharField(max_length=255, label="Ingredient Name")

          
    class Meta:
      model = Ingredient
      fields = ['ingredient_name']