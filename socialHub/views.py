from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
import pymongo
from django.views.decorators.csrf import requires_csrf_token
from myApp.models import UserProfile,Posts,FriendShip,SavePost,LikePost
from django.contrib import messages
from myApp.forms import profileform, postForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from myApp.models import User
from django.http import JsonResponse

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["socialhub"]
col = db["auth_user"]       

def socialHub(request):
     return render(request,'landingPage.html')

@requires_csrf_token
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists!!")
            return render(request, 'login.html')

        if user_obj.check_password(password):
             login(request,user_obj)
             return redirect('home')
        else:
            messages.error(request,"Please Enter Correct Password")
    return render(request,'login.html')
     
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnfpassword')

        if User.objects.filter(username=username).values():
            messages.error(request, "Username already Taken! Please try another")
        elif password == cnf_password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('profile_data')
        else:
            messages.error(request, "Password and confirm password must be same!")
    return render(request,'signup.html')

@login_required(login_url='login_page')
def home(request):      
     if request.method == 'POST':         
          form = postForm(request.POST,request.FILES)
          if form.is_valid():   
            form.instance.user = request.user
            form.save()
            return redirect('home')
     
     #search for new user query
     global searched_users
     searched_users = ''
     if request.method == 'GET' and 'username' in request.GET:
          username = request.GET['username']
          searched_users = UserProfile.objects.filter(user__username__icontains=username)
     
     form = postForm()
     friends_post =  request.GET.get("friends_post")
     recent = request.GET.get("recent_post")
     saved_post = request.GET.get("saved_post")
     liked_post = request.GET.get("liked_post")
     friend_user_ids = FriendShip.objects.filter(user=request.user).values_list('friend_id',flat=True)
     is_saved = SavePost.objects.filter(user=request.user).values_list('post_id',flat=True)
     is_liked = LikePost.objects.filter(user=request.user).values_list('post_id',flat=True)          
     friends_list = FriendShip.objects.filter(user=request.user)
     
     if friends_post:
          posts = Posts.objects.filter(user_id__in=friend_user_ids)
          if recent:
               posts = Posts.objects.filter(user_id__in=friend_user_ids).order_by('-created_at')
     elif recent:
          posts = Posts.objects.exclude(user=request.user).order_by('-created_at')
     elif saved_post:
          posts = Posts.objects.filter(id__in=is_saved)
     elif liked_post:
          posts = Posts.objects.filter(id__in=is_liked)
     else:
          posts = Posts.objects.exclude(user=request.user)
          
     try:
          request.user.userprofile   
     except:
          pass
     
     data = {
          'posts' : posts,
          'user' : request.user,
          'user_profile' :request.user.userprofile,
          'friends' : friends_list,
          'total_friends' : friends_list.count(),
          'friends_list' : friend_user_ids,
          'is_save' : is_saved,
          'is_liked' : is_liked,
          'total_saved_post' : Posts.objects.filter(id__in=is_saved).count(),
          'total_liked_post' : Posts.objects.filter(id__in=is_liked).count(),
          'searched_users'  : searched_users
     }
     return render(request,'home.html',{'data':data,'form':form})

@login_required(login_url='login_page')
def profile(request,username):
     try:
          user_profile = UserProfile.objects.get(user__username=username)
          friends_list =  FriendShip.objects.filter(user__username=username)
     except:
          pass
     
     friend_user_ids = FriendShip.objects.filter(user=request.user).values_list('friend_id',flat=True)
     data = {
          'posts' : Posts.objects.filter(user__username=username),
          'user_profile' : user_profile,
          'total_friends' : friends_list.count(),
          'total_posts':Posts.objects.filter(user__username=username).count(),
          'friends' : friends_list,
          'users' : request.user,
          'friends_list' : friend_user_ids,
          'is_friend' : FriendShip.objects.filter(user=request.user,friend_id__username=username).values_list('user_id',flat=True)
     }
     return render(request,'profile.html',data)

@login_required(login_url='login_page')
def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
def profile_data(request):
    if request.method == 'POST':
        form = profileform(request.POST, request.FILES)

        if form.is_valid():   
            form.instance.user = request.user
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            form = profileform()
    else:
          form = profileform()

    return render(request, 'profile_data.html', {'form': form})

def edit_profile(request):
     if request.method == "POST":
          form = profileform(request.POST,request.FILES,instance=request.user.userprofile)
          if form.is_valid():
               form.save()
               return redirect('home')
     else:
          form = profileform(instance=request.user.userprofile)
     data = {
          'user_profile' :request.user.userprofile,
     }
     return render(request,'edit_profile.html',{'data':data,'form':form})

@login_required(login_url='login_page')
def savepost(request,post_id):
     saved_post_ids = SavePost.objects.filter(user=request.user).values_list('post_id',flat=True)
     post = get_object_or_404(Posts, id=post_id)
     add_post,created = SavePost.objects.get_or_create(user=request.user, post=post)
     add_post.save()
     
     if not created:
        add_post.delete()
        total_saved_post = Posts.objects.filter(id__in=saved_post_ids).count()
        return JsonResponse({'status':'save','total_saved_post':total_saved_post})
   
     total_saved_post = Posts.objects.filter(id__in=saved_post_ids).count()
     return JsonResponse({'status':'saved','total_saved_post':total_saved_post})

@login_required(login_url='login_page')
def likepost(request,post_id):
     post = get_object_or_404(Posts,id=post_id)
     like_post,liked = LikePost.objects.get_or_create(user=request.user,post=post)
     if liked:
          post.no_of_like = post.no_of_like  + 1
          post.save()
     like_post.save()
     
     if not liked:
          post.no_of_like = post.no_of_like - 1
          like_post.delete()
          post.save()
          
     return redirect(request.META.get('HTTP_REFERER','home'))


@login_required(login_url='login_page')   
def add_friend(request,friend_id):    
     add_friend,added = FriendShip.objects.get_or_create(user=request.user, friend_id=friend_id)
     add_friend.save()
     if not added:
        add_friend.delete()
     return redirect('home')
     
@login_required(login_url='login_page')  
def delete_post(request,post_id):
     post = get_object_or_404(Posts,id=post_id)
     post.delete()
     return redirect(request.META.get('HTTP_REFERER','profile'))

@login_required(login_url='login_page')
def delete_account(request,user_id):
       user = get_object_or_404(User, pk=user_id)
       user.delete()
       return redirect('login_page')