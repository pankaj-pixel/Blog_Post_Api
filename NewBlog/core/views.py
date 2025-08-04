from django.shortcuts import render,redirect
from .models import Blog
from .serializers import BlogSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
#from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated
import requests
from django.contrib import messages

# create user authentication
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User




def signupview(request):
    print("request Type : ",request.method)
    print(request.POST.get('username'))
    print(request.POST.get('password1'))
    print(request.POST.get('password2'))
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        print("Create form")
        if form.is_valid():
            print("form is valid")
            user = form.save()
            #login(request,user)
            return redirect('blog_list')
        else:
            print("form error :",form.errors )
    else:
        print("come outside")
        form = UserCreationForm()
    return render(request,'registration/signup.html',{"form":form})    
        

def signinview(request):
    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            return redirect('blog_list')
    
    else:
        form = AuthenticationForm()
    return render(request,'registration/signin.html',{"form":form})        
            
#@login_required 
def logoutview(request):
    logout(request)
    messages.info(request,"Logged out Successfully!")
    return redirect('homepage')








def homepage(request):
    return render(request,'home.html')





@api_view(['GET','POST'])
def blogview(request):

    if request.method =='GET':
        queryset = Blog.objects.all()
        serilize = BlogSerializer(queryset,many=True)
        return Response(serilize.data)
    
    
    elif request.method =='POST':
        queryset = BlogSerializer(data = request.data)

        if queryset.is_valid():
            queryset.save()
            return Response("Post Successfully")


@api_view(['GET', 'PUT', 'DELETE'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def BlogById(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, )

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated successfully."})
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        blog.delete()
        return Response({"message": "Post deleted successfully."})



API_BASE_URL = 'http://127.0.0.1:8000/api/'


def bloghome(request):
    return render(request, 'home.html')

#@login_required 
def blog_list_view(request):
    response = requests.get(API_BASE_URL)
    blogs = response.json() if response.status_code == 200 else []
    return render(request, 'blog_list.html', {'blogs': blogs})

#@login_required 
def admin_blog_list_view(request):
    response = requests.get(API_BASE_URL)
    blogs = response.json() if response.status_code == 200 else []

    return render(request, 'blog_list.html', {'blogs': blogs})


#@login_required 
def admin_blog_detail_view(request, blog_id):
    response = requests.get(f"{API_BASE_URL}{blog_id}")  
    blog = response.json() if response.status_code == 200 else {}
    print("Blog Details:", blog)
    return render(request, 'blog_detail.html', {'blog': blog})
from datetime import datetime



#@login_required 
def admin_blog_create_view(request):
    if request.method == 'POST':
        data = {
            'Blog_title': request.POST.get('Blog_title'),
            'Content': request.POST.get('Content'),
            'Author': request.POST.get('Author'),
            'Status': request.POST.get('Status'),
            'Created_at': datetime.now().isoformat()  
        }
        response = requests.post(API_BASE_URL, json=data)

        if response.status_code in [200, 201]:
            return redirect('blog_list')
        else:
            return render(request, 'blog_create.html', {
                'error': 'Failed to create blog. Please check the fields and try again.'
            })
    return render(request, 'blog_create.html')







def admin_blog_update_view(request, blog_id):
    response = requests.get(f"{API_BASE_URL}{blog_id}")
    blog = response.json() if response.status_code == 200 else {}

    if not blog:
        return render(request, '404.html', status=404)  

    if request.method == 'POST':
        data = {
            'Blog_title': request.POST.get('Blog_title'),
            'Content': request.POST.get('Content'),
            'Author': request.POST.get('Author'),
            'Status': request.POST.get('Status'),
            'Created_at': blog.get('Created_at')  
        }

        update_response = requests.put(f"{API_BASE_URL}{blog_id}", json=data)
        if update_response.status_code == 200:
            return redirect('blog_list')
        else:
            return render(request, 'blog_update.html', {
                'blog': blog,
                'error': 'Update failed. Please try again.'
            })

    return render(request, 'blog_update.html', {'blog': blog})





def admin_blog_delete_view(request, blog_id):
    if request.method == 'POST':
        response = requests.delete(f"{API_BASE_URL}{blog_id}")
        
        if response.status_code == 200:
            messages.success(request, " Blog deleted successfully.")
        else:
            messages.error(request, f"⚠️ Failed to delete blog. Status code: {response.status_code}")
    
    return redirect('blog_list')