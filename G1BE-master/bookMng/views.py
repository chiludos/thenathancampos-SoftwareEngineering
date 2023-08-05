from django.db.models import Q
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm
from .forms import CommentForm
from .forms import MessageForm
from django.http import HttpResponseRedirect
from .models import Book
from .models import MessageBox
from .models import Product
from .models import OrderItem
from .models import Order

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

# User Registration ----------------
class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


# Home Page -----------------
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


# Post a Book ------------------
@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


# Display All Books -------------------------
@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })


# Book Details ------------------------------
@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    comments = book.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.book = book
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form,
                  })


# All books posted by user who is logged in
@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })


# Deleting a book assigned to a user --------
@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


# About Us Page --------------------------
def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


# All Search Functions ------------------------------------------------
@login_required(login_url=reverse_lazy('login'))
def search(request):
    return render(request,
                  'bookSearch/search.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


@login_required(login_url=reverse_lazy('login'))
def searchresults(request):
    query = request.GET.get('q')
    object_list = Book.objects.filter(
        Q(name__icontains=query)
    )
    for b in object_list:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookSearch/searchresults.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': object_list,
                  })


# Forum/ Message Board ----------------------------------------------
def messagebox(request):
    chats = MessageBox.objects.all()

    submitted = False
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/messagebox?submitted=True')
    else:
        form = MessageForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/messagebox.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'chats': chats,
                  })


# Adding Book to Shopping Cart -------------------------------------
@login_required(login_url=reverse_lazy("login"))
def book_add(request, book_id):

    OrderItem.save(Book.objects.get(id=book_id))

    return render(request,
                  'bookMng/book_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


# Purchasing books in Shopping Cart
@login_required(login_url=reverse_lazy("login"))
def purchase(request):
    ordered_items = OrderItem.objects.all()

    return render(request,
                  'bookMng/purchase.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'ordered_item': ordered_items,
                  })
