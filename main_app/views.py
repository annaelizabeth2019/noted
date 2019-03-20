from django.urls import reverse
from django.shortcuts import render, redirect

from .models import Set, Flashcard, Group
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.forms import inlineformset_factory
from .forms import ContactForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import send_mail, BadHeaderError


def home(request):
  set1 = Set.objects.get(id=1)
  set2 = Set.objects.get(id=2)
  set3 = Set.objects.get(id=3)
  
  return render(request, 'home.html', {
    'set1' : set1,
    'set2' : set2,
    'set3' : set3,
  })

def about(request):
  return render(request, 'about.html')

def contact_us(request):
  if request.method == 'GET':
    form = ContactForm()
  else:
    form = ContactForm(request.POST)
    if form.is_valid():
      subject = form.cleaned_data['subject']
      from_email = form.cleaned_data['from_email']
      message = form.cleaned_data['message']
      try:
        send_mail(subject, message, from_email, ['admin@noted.com'])
      except BadHeaderError:
        return HttpResponse('Invalid header found.')
      return redirect('success')
  return render(request, 'contact_us.html', {'form' : form, 'mainclass' : "thin"})

def successView(request):
  return render(request, 'success.html', {'mainclass' : "thin"})

def sets_index(request):
  sets = Set.objects.filter(user = request.user)
  groups = Group.objects.filter(users = request.user)
  return render(request, 'sets/index.html', { 'sets': sets, 'mainclass' : "thin-body", 'groups' : groups } )

@login_required
def unassoc_group(request, user_id, group_id):
  Group.objects.get(id=user_id).groups.remove(group_id)
  return redirect('sets/index.html')

def show_set(request, set_id):
  set = Set.objects.get(id=set_id)
  flashcards = set.flashcard_set.all()
  print('this is set', set)
  return render(request, 'sets/show.html', {
    'set': set, 'flashcards' : flashcards, 'mainclass' : "thin-body"
    })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

#Sets
class SetCreate(CreateView):
  model = Set
  fields = '__all__'
  # redirect user to the flashcard creation page when a set is created
  def get_success_url(self):
    return reverse('create_flashcards', args=(self.object.id,))

class SetUpdate(UpdateView):
  model = Set
  fields = '__all__'

class SetDelete(DeleteView):
  model = Set
  success_url = '/sets/'

#Flashcards
@login_required
def flashcards_index(request, set_id):
  pass

def create_flashcards(request, set_id):
  set = Set.objects.get(id=set_id)
  SetFlashcardFormSet = inlineformset_factory(Set, Flashcard, fields=['question', 'answer'], extra=1, can_delete=True)

  if request.method == 'POST':
    formset = SetFlashcardFormSet(request.POST, instance=set)
    if formset.is_valid():
      formset.save()
      return redirect('create_flashcards', set_id=set_id)

  formset = SetFlashcardFormSet(instance=set)
  return render(request, 'main_app/flashcard_form.html', {
    'set': set,
    'form': formset,
  })

#Groups
def groups_index(request):
  groups = Group.objects.all()
  return render(request, 'groups/index.html', {
    'groups': groups,
  })

class GroupCreate(CreateView):
  model = Group
  fields = '__all__'

def show_group(request, group_id):
  group = Group.objects.get(id=group_id)
  users_not_in_group = User.objects.exclude(id__in = group.users.all().values_list('id'))
  return render(request, 'groups/show.html', {
    'group': group, 
    'users_not_in_group': users_not_in_group,
  })

class GroupList(LoginRequiredMixin, ListView):
  model = Group

def assoc_user(request, group_id, user_id):
  Group.objects.get(id=group_id).users.add(user_id)
  return redirect('show_group', group_id=group_id)

def unassoc_user(request, group_id, user_id):
  Group.objects.get(id=group_id).users.remove(user_id)
  return redirect('show_group', group_id=group_id)