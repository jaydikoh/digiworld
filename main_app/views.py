import requests
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from main_app.models import Cat, Toy
from .forms import FeedingForm

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  response = requests.get('https://catfact.ninja/fact')
  return render(request, 'about.html', {'fact': response.json().get('fact')})

def cat_index(request):
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', { 'cats': cats })

@login_required
def cat_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # Obtain toys that the cat does not have...
  # Get a list of toy ids that the cat does have
  toy_ids_cat_has = cat.toys.all().values_list('id')
  # Query for toys that have ids that are NOT in the above list
  toys = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  # toys = Toy.objects.all()
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 
    'cat': cat,
    'toys': toys, # Pass toys to template
    'feeding_form': feeding_form,
    })

class CatCreate(CreateView, LoginRequiredMixin):
  model = Cat
  # Part of django framework to include all fields
  fields = ['name', 'breed', 'description', 'age']
  # success_url = '/cats/{id}'
  
  def form_valid(self, form):
    form.instance.user = self.request.user # Accessing logged in user
    return super().form_valid(form)
  
class CatUpdate(UpdateView, LoginRequiredMixin):
  model = Cat
  fields = ['breed', 'description', 'age']
  
class CatDelete(DeleteView, LoginRequiredMixin):
  model = Cat
  success_url = '/cats/'

@login_required  
def add_feeding(request, cat_id):
  # request.POST contains the input info submitted in the <form>
  form = FeedingForm(request.POST)
  if form.is_valid():
    # don't save the form to the db until it has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('cat-detail', cat_id=cat_id)

class ToyCreate(CreateView, LoginRequiredMixin):
  model = Toy
  fields = '__all__'
 
class ToyList(ListView, LoginRequiredMixin):
  model = Toy
  
class ToyDetail(DetailView, LoginRequiredMixin):
  model = Toy
   
class ToyUpdate(UpdateView, LoginRequiredMixin):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView, LoginRequiredMixin):
  model = Toy
  success_url = '/toys/'

@login_required    
def associate_toy(request, cat_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('cat-detail', cat_id=cat_id)

@login_required  
def remove_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('cat-detail', cat_id=cat_id)
  
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      #This is how we log a user in
      login(request, user)
      return redirect('cat-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET reqeust, so render signup.html w/ empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as:
  # return render(
  #   request, 
  #   'signup.html',
  #   {'form': form, 'error_message': error_message}
  # )
     