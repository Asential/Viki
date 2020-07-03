import re
import os

from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
    
        file = default_storage.open(f"entries/{title}.md")
        data = file.read().decode("utf-8")
        entry  = {"title": title, "data": data}
        return entry
    except FileNotFoundError:
        return None

def get_filenames():
    
    #Gets all the filenames in a list without their extensions
    
    filenames = []
    directory = r'entries'
    
    for filename in os.listdir(directory):
        
        if filename.endswith(".md"):
            filenames.append(os.path.splitext(filename)[0])
        
        else:
            continue
    
    return filenames