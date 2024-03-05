from django import forms
from django.forms import modelformset_factory
from .models import Recipe, RecipeStep, Ingredient, UnitMeasure, IngredientQuantity
from django.urls import reverse_lazy


class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label="Recipe Title")
    description = forms.CharField(widget=forms.Textarea, label="Recipe Description")
    prep_time = forms.IntegerField(label="Prep Time (minutes)", widget=forms.NumberInput(attrs={'min': 0}))
    cook_time = forms.IntegerField(label="Cook Time (minutes)", widget=forms.NumberInput(attrs={'min': 0}))
    serving_size = forms.IntegerField(label="Serving Size", widget=forms.NumberInput(attrs={'min': 1}))

    def clean_prep_time(self):
        data = self.cleaned_data['prep_time']
        if data < 0:
            raise forms.ValidationError("Prep time cannot be negative.")
        return data

    def clean_cook_time(self):
        data = self.cleaned_data['cook_time']
        if data < 0:
            raise forms.ValidationError("Cook time cannot be negative.")
        return data

    def clean_serving_size(self):
        data = self.cleaned_data['serving_size']
        if data <= 0:
            raise forms.ValidationError("Serving size must be greater than 0.")
        return data
      
    class Meta:
      model = Recipe
      fields = ['title', 'description', 'prep_time', 'cook_time', 'serving_size', 'tags']
      
class RecipeStepForm(forms.ModelForm):
    step = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter step details here...'}), label="Step Details", )
    
    class Meta:
      model = RecipeStep
      fields = ['step']
      
recipe_step_formset = modelformset_factory(RecipeStep, form=RecipeStepForm, extra=1, can_delete=True, max_num=40, validate_max=True)

class IngredientQuantityForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Quantity")
    unit_measure = forms.ModelChoiceField(queryset=UnitMeasure.objects.all(), label="Unit of Measure")

    class Meta:
        model = IngredientQuantity
        fields = ['quantity', 'unit_measure']

ingredient_quantity_formset = modelformset_factory(IngredientQuantity, form=IngredientQuantityForm, extra=1, can_delete=True, max_num=40, validate_max=True)

class IngredientForm(forms.ModelForm):
    ingredient_name = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Start typing to search for an ingredient. If it doesn\'t exist, it will be added.', 'hx-post': reverse_lazy('autocomplete'), 'hx-trigger': 'keyup changed delay:500ms'}), max_length=255, label="Ingredient Name")

          
    class Meta:
      model = Ingredient
      fields = ['ingredient_name']

      
ingredient_formset = modelformset_factory(Ingredient, form=IngredientForm, extra=1, can_delete=True, max_num=40, validate_max=True)


      #           'hx-post': reverse('autocomplete'),  # Use reverse here
      #           'hx-target': 'this',
      #           'hx-trigger': 'keyup changed delay:500ms',
      #           'placeholder': 'Start typing to search for an ingredient. If it doesn\'t exist, it will be added.',
      # }),
      #                                 max_length=255, label="Ingredient Name")
