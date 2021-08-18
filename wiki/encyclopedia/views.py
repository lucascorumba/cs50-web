from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
import random
import markdown2

from . import util

# Form to add a new encyclopedia page
class newPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title...', 'class': 'form-group row', "style": "margin:10px;"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content...', 'class': 'form-group row', "style": "margin:10px;"}))

# Form to edit entries
class editEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "heading": "All Pages"
    })

# Display the contents of the entry
def lookup(request, entry):
    search = util.get_entry(entry)  
    if search:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(search),
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "- Your search didn't match any entry"
        })

# Search entries through search box
def searchBox(request):
    entry = request.GET.get('q')
    roster = util.list_entries()
    if entry not in roster:
        similar = []
        regex = re.compile(f"(?i){entry}")
        for row in roster:
            hit = regex.search(f"{row}")
            if hit:
                similar.append(row)
            else:
                continue
        return render(request, "encyclopedia/index.html", {
            "entries": similar,
            "heading": "Similar Results"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(entry)),
            "title": entry
        })

# Add an encyclopedia entry
def add(request):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            roster = util.list_entries()
            if title in roster:
                return render(request, "encyclopedia/error.html", {
                    "error": f"- The entry '{title}' already exists"
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown2.markdown(util.get_entry(title)),
                    "title": title
                })

    else:
        return render(request, "encyclopedia/add.html", {
            "form": newPageForm()
        })

#Edit an entry
def edit(request):
    form = request.POST
    oldEntry = util.get_entry(form["q"])
    newEntry = editEntryForm(initial = {'content': oldEntry})
    return render(request, "encyclopedia/edit.html", {
        "form": newEntry,
        "title": form["q"]
    })

def saveEdit(request):
    form = request.POST
    util.save_entry(form["name"], form["content"])
    return HttpResponseRedirect(reverse("entry", args=[form["name"]]))
        
# Get random entry
def randomEntry(request):
    roll = random.choices(util.list_entries())
    search = util.get_entry(roll[0])
    return render(request, "encyclopedia/entry.html", {
        'entry': markdown2.markdown(search),
        "title": roll[0]
    })