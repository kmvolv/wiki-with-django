from django.shortcuts import render, redirect
from random import randint

from . import util
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    page = util.get_entry(name)
    if page is None:
        return render(request, "encyclopedia/NullPage.html", {
            "title": name
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content" : markdown.markdown(page),
            "title": name
        })

def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "content" : markdown.markdown(util.get_entry(q)),
            "title": q
        })
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if title=="" or content=="":
            return render(request, "encyclopedia/newentry.html", {
                "message" : "No field can be left empty, please try again!"
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/newentry.html", {
                "message" : "This title already exists, please try again!"
            })
        util.save_entry(title,content)  
        return render(request, "encyclopedia/entry.html", {
            "content" : content,
            "title" : title
        })
    return render(request, "encyclopedia/newentry.html")

def edit(request,title):
    content = util.get_entry(title.strip())
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {
                "message" : "No field can be left empty, please try again!",
                "title": title,
                "content" : content
            })
        util.save_entry(title,content)
        return redirect("entry", name = title)
    return render(request, "encyclopedia/edit.html", {
        "content" : content,
        "title" : title
    })

def random_page(request):
    entries = util.list_entries()
    idx = randint(0,len(entries)-1)
    return redirect("entry", name = entries[idx])
