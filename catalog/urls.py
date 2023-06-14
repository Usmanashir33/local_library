''' the url patterns for the catalog app'''
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index , name='index'),
    path('books',views.BookListView.as_view(),name='books'),
    path('book<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
    path('author<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
    path('authors',views.AuthorListView.as_view(), name='authors'),
    path("mybooks",views.LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    path("totalbooksborrowed", views.TotalBooksBorrowedListView.as_view(), name="total-books-borrowed"),
    path("book/<uuid:pk>/renew" ,views.renew_book_librarian,name='renew-book-librarian'),
    path('author/<int:pk>/delete',views.AuthorDeleteView.as_view(), name='author-delete'),
    path('author/<int:pk>/update',views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/create',views.AuthorCreateView.as_view(), name='author-create'),
    path("book/create",views.BookCreateView.as_view(),name="book-create"),
    path("book/<int:pk>/update",views.BookUpdateView.as_view(),name="book-update"),
    path("book/<int:pk>/delete",views.BookDeleteView.as_view(),name='book-delete'),
]
