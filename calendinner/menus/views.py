from django.shortcuts import render

# Create your views here.
def current_menu(request):
    return render(request, 'menus/current-menu.html')
  
def previous_menu(request):
    return render(request, 'menus/previous-menu.html')
  
def upcoming_menu(request):
    return render(request, 'menus/upcoming-menu.html')