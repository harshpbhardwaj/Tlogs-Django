from django.shortcuts import render, redirect
from datetime import datetime, timedelta
# from home.models import Login
from home.models import Tlogs, Tlog_body, Login, Tlog_comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from home.serializers import HexaSerializers, BodySerializers, CommentSerializers


class HexaViewSet(viewsets.ModelViewSet):
    queryset=Tlogs.objects.all()
    serializer_class=HexaSerializers

    @action(detail=True,methods=['get'])
    def body(self, request, pk=None):
        try:
            t_id=Tlogs.objects.get(pk=pk)
            body=Tlog_body.objects.filter(tlog=t_id)
            body_serializer=BodySerializers(body,many=True,context={'request':request})
            return Response(body_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message':str(e)
            })
    @action(detail=True,methods=['get'])
    def comments(self, request, pk=None):
        try:
            t_id=Tlogs.objects.get(pk=pk)
            comment=Tlog_comment.objects.filter(tlog=t_id)
            comment_serializer=CommentSerializers(comment,many=True,context={'request':request})
            return Response(comment_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message':str(e)
            })
class BodyViewSet(viewsets.ModelViewSet):
    queryset=Tlog_body.objects.all()
    serializer_class=BodySerializers
class CommentViewSet(viewsets.ModelViewSet):
    queryset=Tlog_comment.objects.all()
    serializer_class=CommentSerializers


# Create your views here.
def index(request):
    # data = Tlogs.objects.filter(publish=1).order_by('-id').values()[:6]
    data = Tlogs.objects.order_by('-id').values()[:6]
    my_data = make_tlog_body(data)
    trending = Tlogs.objects.filter( date__gte = datetime.now() - timedelta(days=10)).order_by('-views').values()[:3]
    trending_tlogs = make_tlog_body(trending)
    this_week = Tlogs.objects.filter( date__gte = datetime.now() - timedelta(days=7)).order_by('-views').values()[:2]
    weekly_top = make_tlog_body(this_week)
    this_month = Tlogs.objects.filter( date__gte = datetime.now() - timedelta(days=28)).order_by('-views').values()[:2]
    monthly_top = make_tlog_body(this_month)
    
    tlog_count = Tlogs.objects.all().count()
    users_count = Login.objects.all().count()
    
    context = {
        'tlogs': my_data,
        'tlog_count': tlog_count,
        'users_count': users_count,
        'trending_tlogs': trending_tlogs,
        'weekly_top':weekly_top,
        'monthly_top':monthly_top,
    }
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if request.POST.get('type') == "signup":
            phone = request.POST.get('phone')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            cpassword = request.POST.get('cpassword')
            if password == request.POST.get('cpassword'):
                city = request.POST.get('city')
                state = request.POST.get('state')
                country = request.POST.get('country')
                terms = request.POST.get('terms')
                loginz = Login(email=email, phone=phone, password=password, city=city, state=state, country=country, terms=terms, date=datetime.now())
                loginz.save()
                user = User.objects.create_user(email, email, password)
                user.first_name = fname
                user.last_name = lname
                user.save()
                messages.success(request, 'Hello '+fname+' '+lname+', username '+email+' is added')
            else:
                messages.success(request, 'Incorrect Password!')
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, 'Hello '+email)
            else:
                messages.success(request, 'Incorrect email or password!')
        return redirect('/')
    return render(request, 'index.html', context)

def sign_out(request):
    logout(request)
    messages.success(request, 'User signed out!')
    return redirect('/')

def about(request):
    return render(request, 'pages/basic-grid.html')


def contact(request):
    context = {
        "variable1" : "window",
        "variable2" : "umbrella",
        "variable3" : "cat"
    }
    return render(request, 'pages/basic-grid.html', context)

    
def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        data = Login.objects.filter(email = username).values()[:1][0]
        t_data = Tlogs.objects.filter(email = username).order_by('-id').values()
        my_tlogs = make_tlog_body(t_data)
        context = {
            "profile" : data,
            "tlogs" : my_tlogs
        }
        return render(request, 'profile.html', context)    
def profiles(request, id):
    username = None
    if request.user.is_authenticated:
        username = id
        data = Login.objects.filter(email = username).values()[:1][0]
        t_data = Tlogs.objects.filter(email = username).order_by('-id').values()
        my_tlogs = make_tlog_body(t_data)
        context = {
            "profile" : data,
            "tlogs" : my_tlogs
        }
        return render(request, 'profile.html', context)
        

def view(request, id):
    username = None
    if request.user.is_authenticated:
        t_data = Tlogs.objects.filter(id = id).values()[0]
        t_body = Tlog_body.objects.filter(tlog_id = id).values()
        t_comment = Tlog_comment.objects.filter(tlog_id = id).values()
        Tlogs.objects.filter(id = id).update(views=F("views") + 1)
        # tl_body = {
        #     'body':''
        # }
        # for x in t_body:
        #     body1 = x.body.splitlines()
        #     body2 = []
        #     for i in body1:
        #         if i.startswith('##'):
        #             j = "<h2>" + i + "</h2>"
        #             body2.append(j)
        #         else:
        #             body2.append(i)
        #     body = " ".join(body2)
        #     tl_body.append({'body':body})
        context = {
            "t_id" : id,
            "tlog" : t_data,
            "tlog_body" : t_body,
            "tlog_comment" : t_comment
        }
        return render(request, 'view.html', context)


# function
def make_tlog_body(data):
    my_data = []
    for x in data:
        b_data = Tlog_body.objects.filter(tlog_id=x['id']).exclude(body__isnull=True).exclude(body__exact='').order_by('id').values()[:1]
        body = ''
        if b_data:
            body = b_data[0]['body']
        b_image = Tlog_body.objects.filter(tlog_id=x['id']).exclude(image__isnull=True).exclude(image__exact='').order_by('id').values()[:1]
        image = ''
        if b_image:
            image = b_image[0]['image']
        body1 = body.splitlines()
        body2 = []
        for i in body1:
            if i.startswith('##'):
                j = "<h2>" + i + "</h2>"
                body2.append(j)
            else:
                body2.append(i)
        body3 = " ".join(body2)
        my_data.append(
            {
                't_id': x['id'],
                'title': x['title'],
                'email': x['email'],
                'views': x['views'],
                'date': x['date'],
                'body': " ".join(body3.split(".")[0:1]),
                # 'body' : " ".join(body2),
                'image': image
            }
        )
    return my_data



# form posts
def add_new_comment(request):
    if (request.user.is_authenticated)*(request.method == "POST"):
        email = request.user.username
        #create new tlog
        if 'comment' in request.POST:
            comment = request.POST.get("comment")
            t_id = request.POST.get("tlog_id")
            Tlog_com = Tlog_comment(tlog_id=t_id, comment=comment, email=email, date=datetime.now())
            Tlog_com.save()
            page = 'view/' + str(t_id)
            return redirect(page)

# ajax links
def add_new_tlog(request):
    if (request.user.is_authenticated)*(request.method == "POST"):
        email = request.user.username
        #create new tlog
        if 'title' in request.POST:
            title = request.POST.get("title")
            Tlog = Tlogs(email=email, title=title, date=datetime.now())
            Tlog.save()
            t_id = Tlog.id
            html = title
            return JsonResponse({'t_id':t_id, 'mystring':html})

        #add new para to tlog_body
        elif 'new_body_text' in request.POST:
            t_id = request.POST.get("t_id")
            title = request.POST.get("body_title")
            body = request.POST.get("new_body_text")
            image = ''
            Tlog_data = Tlog_body(tlog_id=t_id, body=body, image=image, email=email, title=title, date=datetime.now())
            Tlog_data.save()
            tbody_id = Tlog_data.id
            html ='<p class="lead" id="para_'+str(tbody_id)+'" onclick="body_edit('+str(tbody_id)+');" style="font-size:16px;">'+body+'</p><textarea class="form-control" id="para_edit_'+str(tbody_id)+'" onblur="body_save('+str(tbody_id)+');" style="display:none;" rows="7" name="para_edit_'+str(tbody_id)+'"></textarea>'
            return JsonResponse({'t_id':t_id,'tbody_id':tbody_id,'mystring':html})

        #add new image to tlog_body
        elif len(request.FILES) != 0:
            t_id = request.POST.get("t_id")
            title = request.POST.get("body_title")
            body = ''
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            image = fs.url(filename)
            Tlog_data = Tlog_body(tlog_id=t_id, body=body, image=image, email=email, title=title, date=datetime.now())
            Tlog_data.save()
            timage_id = Tlog_data.id
            html = '<img src="'+image+'" style="max-height: 200px;" alt="">'
            return JsonResponse({'t_id':t_id,'timage_id':timage_id,'mystring':html})

        #update title in tlog
        elif 'new_title' in request.POST:
            new_title = request.POST.get("new_title")
            t_id = request.POST.get("t_id")
            u_title = Tlogs.objects.get(id=t_id)
            u_title.title = new_title
            u_title.save()
            html = new_title
            return JsonResponse({'t_id':t_id,'mystring':html})

        #update para in tlog_body
        elif 'para_edit_text' in request.POST:
            data = request.POST.get("para_edit_text")
            t_id = request.POST.get("t_id")
            b_id = request.POST.get("b_id")
            u_body = Tlog_body.objects.get(id=b_id)
            u_body.body = data
            u_body.save()
            html = data
            return JsonResponse({'t_id':t_id,'mystring':html})

def delete_tlog(request):
    if (request.user.is_authenticated)*(request.method == "POST"):
        email = request.user.username
        #create new tlog
        if request.POST.get("confirmation"):
            t_id = request.POST.get("tlog_id")
            done = Tlogs.objects.get(id=t_id, email=email).delete()
            return JsonResponse({'deleted':done})