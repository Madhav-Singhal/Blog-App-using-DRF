from django.shortcuts import render, redirect
from .models import Base
from .forms import Blog_form

# Create your views here.

def list(request):
    query = request.POST.get('q', None)
    form = Blog_form()
    object = Base.objects.all()
    if query is not None:
        object = object.filter(title__icontains = query) #we can also add description and other fielsds(des__icontains = query)
    if request.method == 'POST':
        my_form = Blog_form(request.POST or None )
        if my_form.is_valid():
            
            my_form.save()


    return render(request, 'home.html', {'form': form,
                                        'obj': object})




    


