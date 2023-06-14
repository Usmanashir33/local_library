from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django .contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from .models import Book,BookInstance,Genre,Author

@login_required
def index(request):
    ''' view function of the home page of the site'''
    # the session recognition
    num_visits=request.session.get("num_visits",0)
    request.session['num_visits'] =num_visits + 1
    
    # generate counts of some of the main objects
    num_of_books = Book.objects.all().count()
    num_of_instanses = BookInstance.objects.all().count()
    
    #available book status as "a"
    num_of_instanses_available=  BookInstance.objects.filter(status__exact='a').count()
    
    #the all is implaid by default
    num_of_authors = Author.objects.count()
    num_of_genres = Genre.objects.all().count()
    num_of_books_sweet = Book.objects.filter(title__icontains='sweet').count()
    
    context = {
        'num_books':num_of_books,
        "num_instances":num_of_instanses,
        'num_instances_available':num_of_instanses_available ,
        'num_authors':num_of_authors ,
        "num_genres":num_of_genres ,
        'num_book_contains_sweet' :num_of_books_sweet,
        "num_visits":num_visits
    }
    
    #render the HTML template with the data in the context
    return render(request,'catalog/index.html',context=context)

from django.views import generic
class BookListView(generic.ListView):
    model= Book
    paginate_by=0
    
class BookDetailView(generic.DetailView) :
    ''' remember that there is hidden argument passed to this based class '''
    model = Book
    
class AuthorListView(LoginRequiredMixin, generic.ListView):
    login_url="login"
    redirect_field_name = ""
    model = Author
    paginate_by=0
    
    def get_context_data(self, **kwargs):
        context=super(AuthorListView,self).get_context_data(**kwargs)
        context['author_list_number'] =Author.objects.all().count()
        return context
    
class AuthorDetailView(generic.DetailView) :
    model = Author
    
    
class LoanedBooksByUserListView(LoginRequiredMixin , generic.ListView) :
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    #paginate_by=2
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact ="o").order_by('due_back')

class TotalBooksBorrowedListView(PermissionRequiredMixin ,generic.ListView) :
    model=BookInstance
    permission_required =("catalog.can_mark_returned")
    context_object_name ='total_books_borrowed'
    template_name = 'catalog/total_books_borrowed.html'
    paginate_by=0
    
    TotalBooksBorrowed=BookInstance.objects.filter(status__exact="o").order_by("due_back")
    def get_queryset(self) :
        return self.TotalBooksBorrowed
    def get_context_data(self, **kwargs):
        context = super(TotalBooksBorrowedListView,self).get_context_data(**kwargs)
        context["num_books_borrowed"] =len(self.TotalBooksBorrowed)
        return context
    
    
    """ Form views"""
from catalog.forms import RenewBookForm,RenewBookModelForm
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
@login_required
@permission_required("catalog.can_mark_returned",raise_exception=True)
def renew_book_librarian(request,pk) :
    book_instance=get_object_or_404(BookInstance,pk=pk)
    
    'check fro the type of the request'
    if request.method == "POST" :
        form= RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.self.cleaned_data["due_back"]
            book_instance.save()
            return HttpResponseRedirect(reverse('total-books-borrowed'))
    else :
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back':proposed_renewal_date})
        
    context = {
        "form" :form,
        "book_instance" :book_instance
    }
    
    return render(request,'catalog/renew_book_librarian.html',context)

""" the Generic editing Views """
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreateView(PermissionRequiredMixin,CreateView):
    model = Author
    fields=["first_name","last_name","date_of_birth","date_of_death"]
    initial={"date_of_birth":'2000-01-01'}
    success_url = reverse_lazy('authors')
    permission_required=("catalog.can_edit_author")
    
class AuthorUpdateView(PermissionRequiredMixin,UpdateView):
    model=Author
    fields="__all__"
    success_url = reverse_lazy('authors')
    permission_required=("catalog.can_edit_author")
    
class AuthorDeleteView(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required=("catalog.can_edit_author")

""" Editing of the book """
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin

class BookCreateView(LoginRequiredMixin,CreateView):
    model= Book
    login_url="login"
    fields=["title","author","summary","isbn","genre","language"]
    success_url=reverse_lazy("books")

class BookUpdateView(PermissionRequiredMixin,UpdateView):
    model=Book
    permission_required=('catalog.can_edit_book')
    fields=["title","author","summary","isbn","genre","language"]
    success_url=reverse_lazy('books')
    labels={"genre":"Leave Blank if Yours not Available"}
    
class BookDeleteView(PermissionRequiredMixin,DeleteView):
    model=Book
    permission_required=("catalog.can_edit_book")
    success_url=reverse_lazy("books")