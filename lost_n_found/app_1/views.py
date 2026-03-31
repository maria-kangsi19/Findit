from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User  
from django.conf import settings
from .models import Category, Post, Message, Profile
import json
import os


def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def map_page(request):
    return render(request, 'map.html')

def newpost_page(request):
    return render(request, 'newpost.html')

def user_page(request):
    return render(request, 'user.html')

def msg_page(request):
    return render(request, 'msg.html')

def create_page(request):
    return render(request, 'create.html')


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            email = data.get('email')
            password = data.get('password')
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already registered'
                }, status=400)
            
            if User.objects.filter(username=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already taken'
                }, status=400)
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            
            Profile.objects.get_or_create(user=user)
            
            return JsonResponse({
                'status': 'success',
                'user_id': user.id,
                'name': name,
                'message': 'Registration successful'
            }, status=201)
        except Exception as e:
            print(f"Registration error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = email
            
            user = authenticate(username=username, password=password)
            
            if user:
                auth_login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'user_id': user.id,
                    'name': user.first_name or user.username,
                    'email': user.email
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email or password'
                }, status=400)
        except Exception as e:
            print(f"Login error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        posts_count = Post.objects.filter(user=user).count()
        
        profile_pic = None
        if hasattr(user, 'profile') and user.profile.profile_pic:
            profile_pic = user.profile.profile_pic.url
        
        return JsonResponse({
            'id': user.id,
            'name': user.first_name or user.username,
            'email': user.email,
            'profile_pic': profile_pic,
            'join_date': user.date_joined.strftime('%Y-%m-%d'),
            'post_count': posts_count,
            'match_count': 0
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def update_user_profile(request, user_id):
    if request.method == 'PUT':
        try:
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)
            
            if 'name' in data:
                user.first_name = data['name']
                user.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated',
                'name': user.first_name
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_user_posts(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post.id,
                'post_type': post.post_type,
                'description': post.description,
                'category': post.category.name if post.category else None,
                'reward': str(post.reward) if post.reward else None,
                'image': post.image.url if post.image else None,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse(posts_data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def upload_profile_pic(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']
                
                profile, created = Profile.objects.get_or_create(user=user)
                profile.profile_pic = profile_pic
                profile.save()
                
                return JsonResponse({
                    'status': 'success',
                    'image_url': profile.profile_pic.url if profile.profile_pic else None
                })
            
            return JsonResponse({'error': 'No image provided'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        try:
            posts = Post.objects.all().order_by('-created_at')
            posts_data = []
            for post in posts:
                posts_data.append({
                    'id': post.id,
                    'post_type': post.post_type,
                    'description': post.description,
                    'category': post.category.name if post.category else None,
                    'reward': str(post.reward) if post.reward else None,
                    'image': post.image.url if post.image else None,
                    'user_id': post.user.id,
                    'user_name': post.user.first_name or post.user.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            return JsonResponse(posts_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'POST':
        try:
            print("=" * 50)
            print("POST Request Received")
            print("POST data:", request.POST)
            print("FILES:", request.FILES)
            print("=" * 50)
            
            post_type = request.POST.get('post_type')
            description = request.POST.get('description')
            category_name = request.POST.get('category')
            user_id = request.POST.get('user')
            reward = request.POST.get('reward')
            
            if not post_type:
                return JsonResponse({'error': 'post_type is required'}, status=400)
            if not description:
                return JsonResponse({'error': 'description is required'}, status=400)
            if not user_id:
                return JsonResponse({'error': 'user is required'}, status=400)
            if not category_name:
                return JsonResponse({'error': 'category is required'}, status=400)
          
            try:
                user = User.objects.get(id=user_id) 
            except User.DoesNotExist:
                return JsonResponse({'error': f'User with id {user_id} not found'}, status=404)
           
           
            category, created = Category.objects.get_or_create(name=category_name)
           
            post = Post.objects.create(
                post_type=post_type,
                description=description,
                user=user,
                category=category,
                reward=reward if reward else None
            )
           
            if 'image' in request.FILES:
                post.image = request.FILES['image']
                post.save()
                print(f"✅ Image saved to: {post.image.path}")
                print(f"✅ Image URL: {post.image.url}")
            
            return JsonResponse({
                'status': 'success',
                'id': post.id,
                'message': 'Post created successfully',
                'image_url': post.image.url if post.image else None
            }, status=201)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'DELETE':
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Post deleted successfully'
            }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sender_id = data.get('sender')
            receiver_id = data.get('receiver')
            text = data.get('text')
            
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                text=text
            )
            
            return JsonResponse({
                'status': 'success',
                'id': message.id,
                'message': 'Message sent'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)