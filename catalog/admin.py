from django.contrib import admin

# Register your models here.
from . models import Author,Genre,Book,BookInstance,Language


class BookInline(admin.TabularInline):
    model=Book
    extra=0
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','date_of_birth']
    list_filter=['date_of_birth',]
    fieldsets=(
        ("Full Name",{'fields':[("first_name","last_name")]}),
        ("life Time",{'fields':[("date_of_birth",'date_of_death')]})
    )
    inlines=[BookInline]
    
class BookInstanceInline(admin.TabularInline):
    model=BookInstance
    extra = 0
        
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['title','author','language','display_genre']
    list_filter=['genre']
    
    fieldsets =(
        ('Book Info.',{'fields':[('title','author'),('language','genre')]}),
        ('Book Details',{'fields':[('isbn','summary')]})
    )
    inlines =[BookInstanceInline]
    
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=['book','display_book_author',"borrower",'status','due_back','id']
    list_filter=['status','due_back']
    fieldsets = (
        ('Book Info.',{'fields':[('book','id'),'imprint']}),
        ('Availability',{'fields':['status','due_back',"borrower"]})
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

