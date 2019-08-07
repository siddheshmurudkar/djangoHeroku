from django.shortcuts import render # Acts as a middleman between request and response
from .models import Article, Feed
from .forms import FeedForm, CategoryForm # To import a form to allow a form to be created for user to input data
from django.shortcuts import redirect
import feedparser # To assist filtering out the RSS feed to give articles
import datetime
from django.http import HttpResponse
from django.db.models import F

# Create your views here.

def articles_list(request):
   
        articles = Article.objects.all()
        # Recieves all the objects from the article database from models.py
        rows = [articles[x:x+1] for x in range(0, len(articles), 1)]
        # To assist in displaying the articles two in a row
        return render(request, 'news/articles_list.html', {'rows': rows})
        # Redirects the request to articles_list.html and passes 'rows' as a key and rows as a variable
        # Returns the response to the user

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})

def new_feed(request):
    if request.method == "POST":
        # Only if the HTML request is of the POST type then accept the URL
        form = FeedForm(request.POST)
        if form.is_valid():
            # If it is a valid URL then save the URL
            feed = form.save(commit=False)
            # Commit ensures its not stored in the database yet but stored in the memory
            # Used to change something(title in this case)
            existingFeed = Feed.objects.filter(url = feed.url)
            # Checking if the feed URL already exists in the database
            # To avoid duplicate feeds
            if len(existingFeed) == 0:
                feedData = feedparser.parse(feed.url)
                # Convert the given data to a readable format
            else:
                response='The URL already exists'
                return render(request,'news/failed.html' , {'response':response})
                # To inform the user if the URL entered already exists
                # set some fields
            feed.title = feedData.feed.title
            # Save the title of the feed
            feed.save()
                # Save it in the database which is defined in models.py

            for entry in feedData.entries:
                    # Running a loop to access all the articles in the feed
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description
                    d =datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')
                    # Converting the date to the required format(DateTimeField)
                    article.publication_date = dateString
                    article.feed = feed
                    article.save()

            return redirect('news.views.feeds_list')
            # Redirects it to views.feeds_list to display the feeds

    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})

        # First form that the user views which redirects here
    # If it is invalid it doesn't save the form
