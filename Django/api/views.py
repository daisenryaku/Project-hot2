#coding=utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse
from api.forms import EditUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.admin import  User
from django.contrib.auth.hashers import make_password
from api.models import Word,Word_History,Word_Detail,Topic,News,UsertoTopic,UsertoUrl,UsertoWord



# Create your views here.

def getHotWords(request):
    res={}
    words=Word_Detail.objects.order_by('-hot')[0:100]
    for each in words:
        res[each.word.id]={}
        res[each.word.id]['content']=each.word.content
        res[each.word.id]['hot']=each.hot
        res[each.word.id]['fromTopic']=each.fromTopic
        history=Word_History.objects.filter(word=each.word)[0].history
        res[each.word.id]['history']=history

    return JsonResponse(res)

def getHotNews(request):
    res={}
    news=News.objects.order_by('-hot')[0:100]
    for each in news:
        res[each.id]={}
        res[each.id]['content']=each.content
        res[each.id]['hot']=each.hot
        res[each.id]['fromTopic']=each.fromTopic
    return JsonResponse(res)

def getHotTopics(request):
    res = {}
    topics=Topic.objects.all()
    for each in topics:
        res[each.id]={}
        res[each.id]['content']=each.content
        res[each.id]['hot']=each.hot
        res[each.id]['fromNews']=each.fromNews
    return JsonResponse(res)

@login_required
def alterUserUrl(request):
    if request.method=='POST':
        if 'pattern' in request.POST:
            pattern=request.POST['pattern']
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未指定模式'})
        if 'url' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
        if pattern=='add':
            if len(request.POST['url'])>200:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'url过超过200个字符！'})
            else:
                if len(UsertoUrl.objects.filter(url=request.POST['url'],user=request.user))>0:
                    return JsonResponse({'errorCode': 1, 'errorMsg': u'用户已经添加此URL，无法再次添加'})
                else:
                    try:
                        newRelation=UsertoUrl(url=request.POST['url'],user=request.user)
                        newRelation.save()
                        return JsonResponse({'errorCode': 0,'errorMsg':""})
                    except:
                        return JsonResponse({'errorCode': 1, 'errorMsg': u'信息存储失败，发生未知错误'})
        elif pattern=='delete':
            old=UsertoUrl.objects.filter(url=request.POST['url'],user=request.user)
            if len(old)==0:
                return JsonResponse({'errorCode': 2, 'errorMsg': u'用户不存在此URL'})
            else:
                try:
                    old=old[0]
                    old.delete()
                    return JsonResponse({'errorCode': 0,'errorMsg':""})
                except:
                    return JsonResponse({'errorCode': 1, 'errorMsg': u'信息删除失败，发生未知错误'})
    else:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})


@login_required
def alterUsersTopic(request):
    if request.method == 'POST':
        if 'pattern' in request.POST:
            pattern = request.POST['pattern']
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未指定模式'})
        if 'topic' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

        topics = Topic.objects.filter(content=request.POST['topic'])
        if len(topics) == 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
        topic=topics[0]
        if pattern=='add':
            newRelation=UsertoTopic(user=request.user,topic=topic)
            try:
                newRelation.save()
                return JsonResponse({'errorCode': 0,'errorMsg':""})
            except:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'信息存储失败，发生未知错误'})
        elif pattern=='delete':
            olds=UsertoTopic.objects.filter(user=request.user,topic=topic)
            if len(olds)==0:
                return JsonResponse({'errorCode': 2, 'errorMsg': u'用户不存在此话题'})
            try:
                old=olds[0]
                old.delete()
                return JsonResponse({'errorCode': 0,'errorMsg':""})
            except:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'信息删除失败，发生未知错误'})

    else:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

@login_required
def alterUsersWord(request):
    if request.method == 'POST':
        if 'pattern' in request.POST:
            pattern = request.POST['pattern']
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未指定模式'})
        if 'word' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
        words = Word.objects.filter(content=request.POST['word'])
        if len(words) == 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
        word=words[0]
        if pattern == 'add':
            newRelation = UsertoWord(user=request.user, word=word)
            try:
                newRelation.save()
                return JsonResponse({'errorCode': 0,'errorMsg':""})
            except:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'信息存储失败，发生未知错误'})
        elif pattern == 'delete':
            olds = UsertoWord.objects.filter(user=request.user, word=word)
            if len(olds) == 0:
                return JsonResponse({'errorCode': 2, 'errorMsg': u'用户不存在此话题'})
            try:
                old = olds[0]
                old.delete()
                return JsonResponse({'errorCode': 0,'errorMsg':""})
            except:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'信息删除失败，发生未知错误'})

    else:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

@login_required
def getUserInfo(request):
    info = {}
    info['username'] = request.user.username
    info['email'] = request.user.email
    info['urls'] = []
    info['topics']=[]
    info['words']=[]
    for each in UsertoUrl.objects.filter(user=request.user):
        info['urls'].append(each.url)
    for each in UsertoTopic.objects.filter(user=request.user):
        info['topics'].append(each.topic.conetent)
    for each in UsertoWord.objects.filter(user=request.user):
        info['words'].append(each.word.content)

    return JsonResponse(info)

@login_required
def editUserInfo(request):
    form = EditUserForm()
    if request.method == "POST":
        username = request.POST['username']
        password_old = request.POST['password_old']
        user = authenticate(username=username, password=password_old)
        if user is not None:
            # email_new=request.POST['email_new']
            user = User.objects.filter(id=request.user.id)[0]
            form = EditUserForm(request.POST.copy())
            if form.is_valid():
                user.password = make_password(form.cleaned_data['password_new'])
                # user.email=form.cleaned_data['email_new']

                user.save()
                return JsonResponse({'errorCode': 0,'errorMsg':""})
            else:
                errorMsg = []
                for each in form.errors:
                    errorMsg += form.errors[each]
                return JsonResponse({'errorCode': 1, 'errorMsg': errorMsg})  # type(forms.errors)=dict

        return JsonResponse({'errorCode': 1, 'errorMsg': u'用户名或密码错误'})
    else:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})