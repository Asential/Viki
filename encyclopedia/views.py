import markdown2, os
import random

from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from . import util

#--------------------------------------------------------------

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#--------------------------------------------------------------

def entry(request, entry):
    
    # Find and store item if any.
    item = util.get_entry(entry)
 
    # Checks if item exists
    if item:
        
        # Converts markdown text to html
        data = markdown2.markdown(item["data"])
        title = item["title"]
    
        # Sends the item details to entry page
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "data":data
        })

    else:
        # Sets Error true if item does not exist for error page
        error = True
        return render(request, "encyclopedia/entry.html", {
            "error":error
        })

#----------------------------------------------------------------
    
def search(request):
    form = request.POST

    # Stores search query for processing..
    title = form["query"]
    item = util.get_entry(title)
 
    # Checks if item exists to return to item page directly.
    if item:

        return entry(request, item["title"])

    else:

        # Gets the filenames of all the entries from directory.
        filenames = util.get_filenames()

        # Empty list for search results
        results = []
        
        # Checks the query as substring in each filename and 
        # adds to results if matches.
        for name in filenames:
            if title.lower() in name.lower():
                results.append(name)
                
        # Shows all the results if any.        
        if results:
            return render(request, "encyclopedia/index.html", {
                "entries": results
            })

        # Returns the not found page.
        else:

            error = True
            return render(request, "encyclopedia/entry.html", {
                "error":error
            })

#----------------------------------------------------------------

def new(request):

    return render(request, "encyclopedia/new.html")

#----------------------------------------------------------------

def submit(request):
    
    # Get form data from new page creation
    form = request.POST
    title = form["title"]
    content = form["content"]

    # Get all the filenames for comparision
    filenames = util.get_filenames()

    # Compares filenames
    for name in filenames:
        if title.lower() == name.lower():
            print("ERROR Entry already exists")
            return index(request)

    # Sets the name of the file with .md extension
    rename = "%s.md" % title

    # Sets the file path to 'entries'
    filepath = os.path.join('entries', rename)
    
    # Creates and saves file with the content from the form.
    file = open(filepath, "x")
    file.write(content)
    file.close()
    
    return entry(request, title)

#----------------------------------------------------------------

def edit(request, title):

    # Gets the entry details
    item = util.get_entry(title)

    # Store title and content for pre-populating edit page
    main = item["title"]
    content = item["data"]

    return render(request, "encyclopedia/edit.html", {
        "title":main,
        "content":content
    })

#----------------------------------------------------------------

def save(request, title):
    
    form = request.POST
    newContent = form["content"]
    
    # I realized now after writing all the above code that 
    # we were given a function for saving/creating new files :D
    util.save_entry(title, newContent)

    return entry(request, title)

#----------------------------------------------------------------

def rand(request):

    files = util.get_filenames()

    # Puts a random title out of all files
    title = random.choice(files)

    return entry(request, title)