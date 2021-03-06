# Create your views here.
from datetime import datetime



#from django.shortcuts import render

from rest_framework import serializers, viewsets, request, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.template import RequestContext, Template
from django.shortcuts import render, redirect, get_object_or_404  #from tutorial  Beginner
from django.contrib.auth import authenticate, login  #from tutorial  Beginner
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View  #from tutorial  Beginner
from .forms import UserForm  #from tutorial  Beginner

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

import ebooklib
from ebooklib import epub


# Imports must either be relative, like this, or have the full path
from .models import Line, Word, WordsUse
from .serializers import WordSerializer

from bs4 import BeautifulSoup   #for html handling
from bs4 import NavigableString

import re


def home(request):
    loadwords(request)  #calling a function

    soup = BeautifulSoup(open('/home/acilveti92/mysite/mysite/myapp/templates/home.html'))

    print(soup.prettify())

    print("empieza el texto")
    print(soup.get_text())
    text = soup.get_text()
    print("acaba el texto")

    splittext=text.split()
    print(splittext)


    session_key = request.session._session_key
    print("the session key is")
    print(request.session._session_key)

    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    click_user = User.objects.get(pk=uid)
    print("the user is")
    print(click_user)


    print(len(splittext))
    print("here comes the boom")
    print(splittext[0])
#now there should be made a duplicate avoider algorithm to make faster the replacement

    #first filter non alfanumeric letters
    simpletext=set(splittext)   #deletes duplicates items
    print("comparation")
    print(len(splittext))
    print(len(simpletext))
    print(splittext)
    print(simpletext)

    # Remove all strings that contain non-alphanumeric characters
    # \w means a word character (i.e. alphanumeric or underscore)
    # | means or
    # $ means end of string
    word_matcher = re.compile("(?=.*\w)^(\w|'|-)+$")

    unique_words = []
    for word in simpletext:
        # Check if word contains non-alphanumeric characters
        matches = word_matcher.match(word)
        if matches:
            unique_words.append(word)

    print("--------- únique words ---------")
    print(unique_words)

    soupstring = soup.string
    print("print soupstring")
    print(soupstring)

    for tag in soup.find_all(string=re.compile(r"\b%s\b" % "want")):
        print("this is the first tag with want")
        print(tag)
        fixed_text = tag.replace('want', 'I make it!')
        fixed_string = NavigableString(fixed_text)
        new_tag = soup.new_tag("b")
        new_tag.string = tag

        print(type(fixed_string))
        print(type(tag))
        print("this is the fixed text")
        print(fixed_string)
        print(type(tag.parent))
        print(tag.parent)
        tag2=tag.parent




        tag2.string.replace_with(fixed_string)
        print("now it has changed to that")
        print(tag2.string)

    for i in range(0,len(splittext)):
        print(splittext[i])
        print(i)
        #a auxiliary list should be made in order to delete duplications
        print("tick")
        words = Word.objects.filter(english_text=splittext[i])  #there should be something to avoid the error because of the lack of word
        if len(words) is 0:
            #if it is really a word, add to the database and translate it
            print(words)
            print("tock")
        else:
            print(words)
            word_data = WordsUse.objects.filter(user = click_user, english_text = words)
            print("word_data")
            print("tock")
            if len(word_data) is 1:
                # there should be a function to count every apparition of the word, instead of doing one by one
                print("the get has returned the next object")
                print(word_data[0])

                word_data=word_data[0]
                word_data.translation_active = True
                word_data.aparitions += 1

                word_data.save()
                editor = re.sub(r"\b%s\b" % "want" , "traduccion","prueba con want")
                print("el tipo de soup es")
                print(type(soup))
                print(editor)


            else:
                if len(word_data) is 0:
                    word_data = WordsUse(user = click_user, english_text = splittext[i], translation_active = True, aparitions = 1, click = 0) #increment of clicked, and switch translatio_active on ((user=click_user, english_text=words, translation_active = True,
                else:
                    print(" ERROR:there are more than one DB objects." + len(word_data))


    souphtml=soup.prettify()

    template = Template(souphtml)
    context = RequestContext(
        request,
        {'right_now':datetime.utcnow(), "lines" : Line.objects.all()}
        )
    return HttpResponse(template.render(context))


def example(request):
    return render(request, 'index.html')

def example2(request):
    return render(request, 'index2.html')


def hello(request):

    book = epub.read_epub('mysite/mysite/myapp/test.epub')
    print('THE BOOK IS THIS!!!!')
    print(book)
    return HttpResponse('Hello World!')


# Serializers define the API representation.
class LineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Line
        exclude = []

#DESCOMENTARLO
#class WordSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Word
#        exclude = []


# ViewSets define the view behavior.
class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_fields = ['english_text', 'spanish_text']

#user creation
class UserFormView(View):
    form_class =UserForm
    template_name ='registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('http://acilveti92.pythonanywhere.com/')

            return render(request,self.template_name,{'form':form})


class wordajax(APIView):
#IT ONLY WORKS WITH GET, WITH POST 403 ERROR
    def get(self, request):

        datos= request.query_params
        datos=datos.copy()
        print("the word is")
        print(datos['palabra'])
        words = Word.objects.get(english_text=datos['palabra'])
        print("the object words is ")
        print( words)
        serializer = WordSerializer(words)

        session_key = request.session._session_key
        print("the session key is")
        print(request.session._session_key)

        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        click_user = User.objects.get(pk=uid)
        print("the user is")
        print(click_user)
        word_data = WordsUse.objects.filter(user = click_user, english_text = words)    #english text has to be an object.
        if len(word_data) is 1:
            print("the get has returned the next object")
            print(word_data[0])
            word_data=word_data[0]
            word_data.translation_active = True
            word_data.click += 1
        else:
            if len(word_data) is 0:
                word_data = WordsUse(user = click_user, english_text = words, translation_active = True, aparitions = 0, click = 1) #increment of clicked, and switch translatio_active on ((user=click_user, english_text=words, translation_active = True,
            else:
                print(" ERROR:there are more than one DB objects." + len(word_data))


        #pruebaword = WordsUse.objects.get(aparitions=0)

        #pruebaword.user= click_user
        #pruebaword.english_text= words
        #pruebaword.translation_active=True
        #pruebaword.aparitions=0
        #pruebaword.click=0

        #task to do:
        #if-else statement for avoid repeatin word_data
        #clean the code
        #increment the click record
        #switch of the translation
        #in javascript change tehe code in the replace part.




        print("the word_data object is")
        print(word_data)
        print("this is a test-2")
        word_data.save()



        #word_data.clicked += 1
        #word_data.save()
        #print("the word_data object is")
        #print(word_data)
        #print("fin")

        return Response(serializer.data)

def newpagewords(request):
    test = "I want"
    test=test.lower()
    words = test.split()

    print(words)
    for i in range(0,len(words)):
        print(words[i])


    session_key = request.session._session_key
    print("the session key is")
    print(request.session._session_key)

    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    click_user = User.objects.get(pk=uid)
    print("the user is")
    print(click_user)


    for i in range(0,len(words)):

        words_obj = Word.objects.get(english_text = words[i])
        word_data = WordsUse.objects.filter(user = click_user, english_text = words_obj)

        if len(word_data) is 1:
            word_data_obj=word_data[0]
            print("the get has returned the next object")
            print(word_data_obj)
            word_data_obj.aparitions += 1
            word_data_obj.save()
        else:
            if len(word_data) is 0:
                print(" there was not word in DB")
                word_data = WordsUse(user = click_user, english_text = words, translation_active = True, aparitions = 1, click = 0) #increment of clicked, and switch translatio_active on ((user=click_user, english_text=words, translation_active = True,
                word_data.save()
            else:
                print(" ERROR:there are more than one DB objects." + len(word_data))

        # when certain number of aparitions are done, the translation should be switched off. task to do in the future



    print(words)
    print("this is a test-1")
    return HttpResponse("I want")

def loadwords(request):

    print("you are right")
    return HttpResponse("you are right")




