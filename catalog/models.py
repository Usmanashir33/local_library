from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model) :
    """ model of the genre of all the books in the library"""
    name = models.CharField(max_length=200,help_text='Enter the genre of the book')
    
    def __str__(self):
        return self.name

from django.urls import reverse
class Book(models.Model) :
    """ model representing a book but not a specipic book or copy"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author",on_delete= models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000,help_text='Write a brief discription about the book')
    isbn = models.CharField("ISBN",max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre =models.ManyToManyField('Genre',help_text="select the genre of this book")
    language= models.ForeignKey('Language',on_delete=models.CASCADE)
   
    def display_genre(self):
        return "".join(gen.name for gen in self.genre.all())
        ''' you can also use this syntax
        to extract the exact genre of tghe book from the other genres hence its the many to many relation
        and this is the rule
        my_genre= [gen.name for gen in self.genre.all()]
        return my_genre'''
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])
    class Meta :
        permissions=(
            ("can_edit_book","can edit any book"),
        )
import uuid
class BookInstance(models .Model):
    """ the model that manages all the books available in the library 
    and also the informatin about the book
    """
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique id for this book across all the library')
    book=models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    borrower = models .ForeignKey(User,on_delete=models.SET_NULL , null=True , blank = True )
    
    LOAN_STATUS=[
        ("m",'Maintainance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved')
    ]
    status=models.CharField(max_length=1,choices=LOAN_STATUS,default='m',help_text='Book Availability in the LIbrary')
    
    class Meta :
        ordering =['due_back']
        permissions = (
            ("can_mark_returned","Set book as returned "),
        )
    
    @property
    def is_overdue(self ):
        """determine if the book is over due or not  """ 
        return bool(self.due_back and date.today() > self.due_back)
        
    def display_book_author(self) :
        return self.book.author 
      
    def __str__(self):
        return f"{self.id} ({self.book.title})"
    
class Author (models.Model):
    """ models representing the author of each book in the library"""
    first_name = models.CharField(max_length=50,help_text='Write your first name e.g usman')
    last_name = models.CharField(max_length=50,help_text='Write your last name e.g ashir')
    date_of_birth = models.DateField('D.O.B',help_text='Write your date of birth e.g 14/03/2001',blank=True,null=True)
    date_of_death = models.DateField('Died',help_text='Write date of Dirth e.g 14/03/2001',blank=True,null=True)
    
    class Meta :
        ordering=['last_name','first_name']
        permissions =(
         ('can_edit_author',"can_edit_any_author"),
     )
        
    def get_absolute_url(self):
        return reverse ("author-detail",args=[str(self.id)])
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class Language(models.Model) :
    """ model that represent the language of the books in the library"""
    name = models.CharField('Lang.',max_length=50,help_text='Write the language of the book (e.g Hausa)')
    
    class Meta :
         verbose_name_plural = 'Languages'
    def __str__(self):
        return self.name[:3]+ "."