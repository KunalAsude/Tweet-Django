from django.shortcuts import render
from .models import Message
from .forms import MessageForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

def index(req):
    return render(req,'index.html')

def tweet_list(req):
    query = req.GET.get('query')
    tweets = Message.objects.all().order_by('-created_at')
    if query:
        tweets = tweets.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        )

    return render(req,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(req):
    if req.method=='POST':
        form = MessageForm(req.POST,req.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('tweet_list')
            


    else:
        form = MessageForm()
        return render(req,'tweet_form.html',{'form':form}) 

@login_required    
def tweet_edit(req,tweet_id):
    tweet=get_object_or_404(Message,pk=tweet_id,user=req.user)
    if req.method == 'POST':
        form = MessageForm(req.POST,req.FILES,instance=tweet)
        tweet = form.save(commit=False)
        tweet.user = req.user
        tweet.save()
        return redirect('tweet_list')
        
    else :
        form = MessageForm(instance=tweet)
        return render(req,'tweet_form.html',{'form':form}) 

@login_required  
def tweet_delete(req,tweet_id):
    tweet = get_object_or_404(Message,pk=tweet_id,user=req.user)
    if req.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(req,'tweet_confirm_delete.html',{'tweet':tweet}) 


def register(req):
    if req.method=='POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(req,user)
            return redirect('tweet_list')
            
    else:
        form=UserRegistrationForm()

    return render(req,'registration/register.html',{'form':form}) 



