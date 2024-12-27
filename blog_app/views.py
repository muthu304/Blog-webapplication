import logging
from django.core.checks import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from blog_app.models import Post as post
from blog_app.models import Category as category
from blog_app.models import aboutus
from .forms import contactform, registerform, loginform, forgotpasswordform, postform
from django.contrib import messages as message
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
	blog_title = "Top Animes"
	
	# getting data from post model
	all_posts = post.objects.filter(is_published = True)
	paginator= Paginator(all_posts,5)
	page_number = request.GET.get('page',1)
	page_obj = paginator.get_page(page_number)
	return render(request, 'index.html',{'blog_title':blog_title,'page_obj':page_obj})


def detail(request,slug):
	# static data
	# post = next((item for item in posts if item['id'] == int(post_id)), None)
	try:
		# getting data from model by post id
		Post = post.objects.get(slug=slug)
		
		related_posts = post.objects.filter(category = Post.category).exclude(pk=Post.id)
		
	
	except Post.DoesNotExist:
		raise Http404("Post Does not Exist!")
	
	# logger = logging.getLogger("TESTING")
	# logger.debug(f'post variable is {post}')=
	return render(request, 'detail.html', {'Post': Post,'related_posts':related_posts})


#custom 404 error page

def custom_page_not_found(request,exception):
	return render(request,'404.html',status=404)

def about(request):
	about_content = aboutus.objects.first().content
	return render(request,'about.html',{'about_content':about_content})

def contact(request):
	if request.method == "POST":
		print("POST method")
		form = contactform(request.POST)
		if form.is_valid():
			logger = logging.getLogger("Testing")
			logger.debug(f"Post data is: Name={form.cleaned_data['name']}, "
			             f"Email={form.cleaned_data['email']}, "
			             f"Message={form.cleaned_data['message']}")
	
	return render(request,'contact.html')

def register(request):
	form = registerform()
	if request.method == "POST":
		form = registerform(request.POST)
		if form.is_valid():
			user = form.save(commit=False) #user data created
			user.set_password(form.cleaned_data['password'])
			user.save()
			message.success(request,'Thankyou for Registration, You can login anytime')
			return redirect("/login/")

	return render(request,'register.html',{'form':form})


def login(request):
	form = loginform()
	if request.method == "POST":
		form = loginform(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				auth_login(request, user)
				print("login success")
				return redirect("/dashboard")
	
	return render(request,'login.html',{'form':form})


def dashboard(request):
	blog_title = "MY POSTS"
	all_posts = post.objects.filter(user = request.user)
	
	
	paginator = Paginator(all_posts, 5)
	page_number = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_number)
	return render(request,'dashboard.html',{'blog_title':blog_title, 'page_obj':page_obj})

def logout(request):
	auth_logout(request)
	return redirect("index")

def forgot_password(request):
	if request.method == 'POST':
		form = forgotpasswordform(request.POST)
	return render(request,'forgot_password.html')

@login_required
def newpost(request):
    categories = category.objects.all()
    form = postform()
    if request.method == 'POST':
        #form
        form = postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    return render(request,'newpost.html', {'categories': categories, 'form': form})

@login_required
def edit_post(request,post_id):
	categories = category.objects.all()
	Post = get_object_or_404(post, id=post_id)
	form = postform()
	
	if request.method == 'POST':
		form = postform(request.POST, request.FILES, instance=Post)
		if form.is_valid():
			form.save()
			message.success(request, 'Your Post is updated')
			return redirect('dashboard')
		
	return render(request, 'edit_post.html', {'categories': categories, 'post': Post, 'form':form})
	
@login_required
def delete_post(request,post_id):
	Post = get_object_or_404(post, id=post_id)
	Post.delete()
	message.success(request,'Your Post has been deleted')
	return redirect('dashboard')
@login_required
def publish_post(request,post_id):
	Post = get_object_or_404(post, id=post_id)
	Post.is_published = True
	Post.save()
	message.success(request, 'Post Published Succesfully!')
	return redirect('dashboard')