from django import forms
from .models import Recipe, RecipeStep, Ingredient, UnitMeasure, IngredientQuantity

class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label="Recipe Title")
    description = forms.CharField(widget=forms.Textarea, label="Recipe Description")
    prep_time = forms.IntegerField(label="Prep Time (minutes)")
    cook_time = forms.IntegerField(label="Cook Time (minutes)")
    serving_size = forms.IntegerField(label="Serving Size")
    # Assuming image upload functionality is implemented elsewhere
    # image_filename = forms.ImageField(label="Recipe Image")

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
    step = forms.CharField(widget=forms.Textarea, label="Step Details")
    
    class Meta:
      model = RecipeStep
      fields = ['step']

class IngredientQuantityForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), to_field_name='ingredient_name', label="Ingredient")
    quantity = forms.IntegerField(label="Quantity")
    unit_measure = forms.ModelChoiceField(queryset=UnitMeasure.objects.all(), label="Unit of Measure")
    
    class Meta:
      model = IngredientQuantity
      fields = ['ingredient', 'quantity', 'unit_measure']
