from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show sll topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank 
        form = TopicForm()
    else:
        # POST data submitted; process data. 
        form = TopicForm(data=request.POST)
        if form.is_valid():
            #modify the new topic before saving it to the database. Then set the new topic’s owner attribute to the current user. Finally call save() on the topic instance just defined.
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    # check that the current user owns the entry’s topic before saving the new entry.
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # create a new entry object and assign it to new_entry without saving it to the database yet.
            new_entry = form.save(commit=False)
            # set the topic attribute of new_entry to the topic we pulled from the database at the beginning of the function
            new_entry.topic = topic
            new_entry.save()
            # requires two arguments—the name of the view we want to redirect to and the argument that view function requires. 
            # Here, we’re redirecting to topic(), which needs the argument topic_id. 
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    # Display a blank or invalid form. This code will execute for a blank form or for a submitted form that is evaluated as invalid
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    #retrieve the entry and the topic associated with this entry.
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #then check whether the owner of the topic matches the currently logged in user.
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

# Refactoring: There are two places where the user associated with a topic matches the currently logged-in user. 
def check_topic_owner(topic, user):
    """Make sure the currently logged-in user owns the topic that's 
    being requested.

    Raise Http404 error if the user does not own the topic.
    """
    if topic.owner != user:
        raise Http404















