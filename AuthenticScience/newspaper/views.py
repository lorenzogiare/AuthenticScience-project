from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchBarForm, AuthorLoginForm, AuthorRegistrationForm, NewArticleForm, ArticleDetailsRequestForm
from .models import Article, ArticleDetailsRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .utils import *
from .ip_management import *
from django.contrib.messages import get_messages


# manages the view of the list of articles, including a search bar
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')

    if request.method == 'POST':
        form = SearchBarForm(request.POST)

        # orders the articles
        if request.POST['articles_order'] == 'LEAST RECENT':
                articles = Article.objects.all().order_by('published_date')

        if form.is_valid():
            
            # filters of the articles shown
            if request.POST['search_filter'] != '':
                articles = articles.filter(title__contains=request.POST['search_filter'])

            if request.POST['author_filter'] != 'any':
                articles = articles.filter(author=request.POST['author_filter'])


    else:
        form = SearchBarForm()
    
    return render(request, 'newspaper/article_list.html', {'form':form, 'articles': articles, "articles_ages": get_articles_age(articles, timezone.now())})

# manages the author login view
def author_login(request):
    
    if request.method == 'POST':
        form = AuthorLoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            # if user exists, checks for his previous IP and sends a warning if needed
            if user is not None :

                # checks if the user logging in is an authenticated author
                if not User.objects.get(username=request.POST['username']).profile.verified_author:
                    messages.error(request,'you are not a verified author!')

                    return redirect('/author/login/')

                login(request, user)
                user_data = get_client_data()
                register_ip(user_data, request.POST['username'], timezone.now())
                ip_warning(request.POST['username'])

                return redirect('/articles/')
                
            else:
                # Return an 'invalid login' message.
                messages.error(request,'incorrect username or password')

                return redirect('/author/login/')
            
    else:

        form = AuthorLoginForm()

    return render(request, 'newspaper/author_login.html', {'form':form, 'url_now':'/login', 'messages':get_messages(request)})

# manages the view of a specific article
def article_details(request, pk):
    article = Article.objects.get(pk=pk)
    context = (request.user == article.author) 

    return render(request, 'newspaper/article_details.html', {'article': article, 'user_is_author':context})

# manages the author registration view
def author_registration(request):
   
    if request.method == 'POST':
        form = AuthorRegistrationForm(request.POST)

        if form.is_valid():
            username = request.POST['username']

            # checks if username is already taken
            if User.objects.filter(username=username).exists():
                
                messages.error(request,'Username already taken')

            #if username not taken (creates user and logs in)
            else:
                user = User.objects.create_user(
                    username = username,
                    password = request.POST['password'], 
                    email = request.POST['email'])

                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                login(request, user)

                return redirect('/articles/')
            
            '''
            # checks if username is already taken
            try:
                user = User.objects.get(username=request.POST['username'])                
                messages.error(request,f'Username {user} already taken')


                return render(request, 'newspaper/author_login.html', {'form': form, 'messages':get_messages(request)})
                
            #if username not taken (creates user and logs in)
            except User.DoesNotExist:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password'], email = request.POST['email'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                login(request, user)

                return redirect('/articles/')
            '''
    else:

        form = AuthorRegistrationForm()

    return render(request, 'newspaper/author_login.html', {'form':form, 'messages':get_messages(request)})

# manages view for publishing new articles, login is required
@login_required(login_url='/author/login/')
def new_article(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
            
        # once the article has been created, a transaction is send and the article published
        if form.is_valid() :
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.status = 'P'
            article.save()
            article.publish()
            article.tx_id = sendTransaction(sha_from_json_of_article(article))
            article.save()

            
            return redirect('article_details', pk=article.pk)

    else:
        form = NewArticleForm()
    
    return render(request, 'newspaper/edits_new.html', {'form': form, 'url_now':'/new'})

# manages the editing view
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # only accessible if the currently logged-in user is the author
    if request.user == Article.objects.get(pk=pk).author:

        if request.method == "POST":

            form = NewArticleForm(request.POST, instance=article)

            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.published_date = timezone.now()
                article.save()

                #edits the json file as well
                with open(f'newspaper/static/json_from_articles/{pk}.json', 'r') as myjsonfile:
                    data = json.load(myjsonfile)

                data['description'] = request.POST['description']
                data['title'] = request.POST['title']
                data['content'] = request.POST['content']

                with open(f'newspaper/static/json_from_articles/{pk}.json', 'w') as myjsonfile:
                    json.dump(data, myjsonfile)
 
                return redirect('article_details', pk=article.pk)
        else:
            form = NewArticleForm(instance=article)

        return render(request, 'newspaper/edits_new.html', {'form': form, 'url_now':'/edit', 'article_title':article.title})
    
    return render(request, 'newspaper/article_details.html', {'article': article})

# manages the logout action
def author_logout(request):
    logout(request)

    return redirect('/articles/')

# manages the data request view (for a specific article)
def details_json(request, pk):

    if request.method == 'POST':
        form = ArticleDetailsRequestForm(request.POST)

        if form.is_valid():  
                #creates a new ArticleDetailRequest object
                detail_req = ArticleDetailsRequest.objects.create(
                    user = str(request.user),
                    title_requested = (Article.objects.get(pk=pk)).title,
                    pk_requested = pk,
                    id_string = request.POST['id_string']
                )
                detail_req.save()
                
                #gets the json data to be shown in the template
                with open(f'newspaper/static/json_from_articles/{pk}.json', 'r') as json_data:
                    data_list = json.load(json_data)

                return render(request, 'newspaper/details_json.html', {'data' : data_list.items(), 'article': Article.objects.get(pk=pk)})
    else:
        form = ArticleDetailsRequestForm()

    return render(request, 'newspaper/details_json.html', {'form': form , 'article': Article.objects.get(pk=pk)})

