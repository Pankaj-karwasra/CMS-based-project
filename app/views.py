from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from .models import AddBlog,Profile,ContactInfo
from .forms import AddForm,ProfileForm,ContactForm,CustomerRegistrationForm,LoginForm
from django.views import View
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

# Create your views here.

def home(request):
    return render(request,'app/index.html')


def about(request):
    return render(request,'app/about.html')

def service(request):
    return render(request,'app/service.html')


# Blog
@login_required(login_url='login') 
def blog(request):
    data = AddBlog.objects.all()
    print(data)
    return render(request,'app/blog.html',{'data':data})


# Add Blog
def add_blog(request):
    if request.method == 'POST':
        fm = AddForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()  
            return redirect('your_blog')  
    else:
        fm = AddForm()

    return render(request, 'app/add_blog.html', {'form': fm})

# Full Blog
def full_blog(request,id):
    blog = get_object_or_404(AddBlog,id=id)
    return render (request,'app/full_blog.html',{'blog':blog})


# Your Blog
@login_required(login_url='login') 
def your_blog(request):
    user_blogs = AddBlog.objects.filter(author=request.user)
    print(user_blogs)
    return render(request, 'app/your_blog.html', {'blogs': user_blogs})


# Update Blog
def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi = AddBlog.objects.get(pk=id)
            form = AddForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = AddBlog.objects.get(pk=id)
            form = AddForm(instance=pi)
        return render(request,'app/update_blog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


# Delete Blog
def delete_post(request,id):
        if request.method == 'POST':
            pi = AddBlog.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/add_blog')


# Contact
def contact(request):
    if request.method == 'POST':
        fm = ContactForm(request.POST)
        if fm.is_valid():
            fm.save()
           
            return render(request, 'app/contact.html', {'form': fm, 'message': 'Your message has been sent!'})
    else:
        fm = ContactForm()  

    return render(request, 'app/contact.html', {'form': fm})


def contact_view(request):
    contact_info = ContactInfo.objects.first() 
    context = {'contact_info': contact_info}
    return render(request, 'app/contact.html', context)
       

# Profile
@login_required(login_url='login') 
def profile_section(request):
    # Fetch or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'profile': profile,
    }
    return render(request, 'app/profile_section.html', context)

# Update Profile
@login_required(login_url='login') 
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_section')  # Redirect to profile view after updating
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'app/update_profile.html', {'form': form})




# Signup
class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/signup.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'app/signup.html', {'form':form})


# Login
class CustomLoginView(auth_views.LoginView):
    template_name = 'app/login.html' 
    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return redirect('home')


# Logout Page
def logout_view(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


# Delete Account
def delete_account(request):
    if request.method == 'POST':
        user = request.user  
        user.delete() 
        logout(request)  
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  
    return render(request, 'app/delete_account.html')


