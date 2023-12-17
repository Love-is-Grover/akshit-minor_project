from django.shortcuts import render,HttpResponse,redirect
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Feedback,Image,Audio
from image_generator.settings import OPENAI_API_KEY
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse
import requests
from pyunsplash import PyUnsplash
from gtts import gTTS

# Create your views here.
def home(request):
    try:
        fbks = Feedback.objects.all()
    except:
        fbks = None
    content = {
        "fbks" : fbks
    }
    return render(request,"index.html",content)

@login_required(login_url="login")
def generator(request):
    # import openai
    # openai.api_key = OPENAI_API_KEY
    obj = None
    # if openai.api_key is not None and request.method == "POST":
    #     text = request.POST.get('imagination')
    #     response = openai.Image.create(
    #         prompt = text,
    #         size = "256x256"
    #     )
    #     print(response)
    #     img_url = response['data'][0]['url']
    #     response = requests.get(img_url)
    #     img_file = ContentFile(response.content)
    if request.method == "POST":
        
        text = request.POST.get('imagination')
        # from pexels_api import API
        # PEXELS_API_KEY = 'VWaAqUDxggERgznZNrfQC69SEvyeylzpbeXEMsRSkyt0ukYaFrwd0a0L'
        # api = API(PEXELS_API_KEY)
        # api.search(text, page=1, results_per_page=1)
        # photos = api.get_entries()
        # photo = photos[0].url
        # print(photo)
        latest = ((Image.objects.last()).id)+1
        # print("latest id  : ",latest.id)
        fname = f"image-{latest}.jpg"
        # response = requests.get(photo)
        # print(response)
        # img_file = ContentFile(response.content)
        # obj = Image(phrase = text)
        # obj.ai_image.save(fname,img_file,save = True)
        # obj.save()
        # print(obj)
        # obj = Image.objects.filter(phrase = "computer system in space").first()
        UNSPLASH_ACCESS_KEY = "R6fIJDkWqcuQLKMgi2pgHCUy7MWtrmWOflBv-9ajgqo"
        pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
        photos = pu.photos(type_='random', count=1, featured=True, query=text)
        [photo] = photos.entries
        print(photo.id, photo.link_download)
        
        response = requests.get(photo.link_download, allow_redirects=True)
        # print(response.content)
        img_file = ContentFile(response.content)
        print(img_file)
        
        
        
        obj = Image(phrase = text)
        obj.ai_image.save(fname,img_file,save = True)
        obj.save()

    return render(request,"generator.html",{"object":obj})


def register(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        form = CustomUserForm()
        if request.method == "POST":
            form = CustomUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                messages.success(request,"Account created successfully")
                return redirect("login")
        content = {
            'form' : form,
            'title' : "Register",
        }
        return render(request,"register.html",content)
    
    
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password= password)
            if user is not None:
                auth_login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("home")
            else:
                messages.error(request,"Invalid Username and Password")
                return redirect('login')
        content = {
            "title" : "Log-In"
        }
        return render(request,"login.html",content)
    
    
@login_required(login_url="login")
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("home")


@login_required(login_url="login")
def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        message = request.POST.get('message')

        fbk = Feedback(
            name = name,
            email = email,
            phone = phone,
            message = message,
        )
        messages.success(request,"Feedback sent Successfully!")
        fbk.save()
    return redirect("home")


@login_required(login_url="login")
def download_file(request, file_id):
    file_obj = get_object_or_404(Image, id=file_id)

    if file_obj.ai_image.file_type == 'png':
        # For PNG images, set the content type explicitly
        response = FileResponse(file_obj.file, content_type='image/png')
    else:
        # For other file types, let Django determine the content type
        response = FileResponse(file_obj.file)

    # Set the Content-Disposition header to trigger a file download
    response['Content-Disposition'] = f'attachment; filename="{file_obj.phrase}"'
    
    return response




@login_required(login_url="login")
def audio(request):
    text = request.POST.get('text')
    print(text)
    if text:
        tts = gTTS(text)
        tts.save(f"media/audio/audio.mp3")
        music = "ok"
        context = {
            'music' : music,
        }
        return render(request,"audio.html",context)
    else:
        return render(request, 'audio.html')
