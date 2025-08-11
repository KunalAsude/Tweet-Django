from django.shortcuts import render
from .models import Message
from .forms import MessageForm
from django.shortcuts import get_object_or_404,redirect

def index(req):
    return render(req,'index.html')

def tweet_list(req):
    tweets = Message.objects.all().order_by('-created_at')

    return render(req,'tweet_list.html',{'tweets':tweets})

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
    
def tweet_delete(req,tweet_id):
    tweet = get_object_or_404(Message,pk=tweet_id,user=req.user)
    if req.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(req,'tweet_confirm_delete.html',{'tweet':tweet}) 

