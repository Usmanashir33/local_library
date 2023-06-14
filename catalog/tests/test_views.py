from django.test import TestCase
from django.urls import reverse
from catalog.models import Author

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create 13 authors for pagination test
        number_of_authors = 13
        
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f"Usman {author_id}",
                last_name=f"Ashir {author_id}"
            )
            
    def test_view_url_exits_at_desired_location(self):
        response= self.client.get("/catalog/authors/")
        self.assertEqual(response.status_code,200)
        
    def test_View_url_accessible_by_name(self):
        response=self.client.get(reverse("authors"))
        self.assertEqual(response.status_code,200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"catalog/author_list.html")
        
    def test_pagination_is_10(self):
        response= self.client.get(reverse("authors"))
        self.assertEqual(response.status_code,200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["author_list"]),10)
        
    def test_lists_all_authors(self):
        response = self.client.get(reverse("authors")+"?page=2")
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["author_list"]),3)
        
        
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from catalog.models import Book,BookInstance,Genre,Language

class LoanedBookInstanceByUserListView(TestCase):
    def setUP(self):
        
        #create 2 users
        test_user1 = User.objects.create_user(
            username='testuser1',
            password= '1145Man11'
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password= '1145Man11'
        )
        test_user1.save()
        test_user2.save()
        
        #create book
        test_author = Author.objects.create(
            first_name = "usman",
            last_name="Ashir"
        )
        test_genre= Genre.objects.create(name="Romabntic")
        test_language= Language.objects.create(name="Arabic")
        test_book=Book.objects.create(
            title="Social Network",
            summary='My book in social nmetwork',
            isbn='ABCDFGHJK',
            author=test_author,
            language=test_language,
        )
        #create genre as post because its many to many realtion ship
        genre_objects_for_book= Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        #craete 30 book instance objects
        number_of_books_copies = 30
        for book_copy in range(number_of_books_copies):
            #craettions
            return_date= timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book= test_book,
                imprint= 'Unlikely imprint 2023',
                due_back = return_date,
                the_borrower= the_borrower,
                status= status,
            )
            
    def test_redirec_if_not_logged_in(self):
        response = self.client.get(reverse("my-borrowed"))
        self.assertRedirects(response,"/accounts/login/?next=/catalog/mybooks")
            
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1',password='1145Man11')
        response = self.client.get(reverse("my-borrowed"))
            
        self.assertEqual(str(response.context['user']),"testuser1")
        self.assertEqual(response.status_code,200)
        self.assertTemplatedUsed(response,"catalog/bookinstance_list_borrowed_user,html")
            
    def test_only_borrowed_books_in_the_list(self):
        login = self.client.login(username='testuser1',password='1145Man11')
        response = self.client.get(reverse("my-borrowed"))
        
        self.assertEqual(response.context['user'],'testuser1') 
        self.assertEqual(response.status_code,200)   
        
        self.assertTrue("bookinstance_list" in response.context)
        self.assertEqual(len(response.context['bookinstance_list']) , 0)
        
        # lets change all the books to be on loan
        books = BookInstance.objects.all()[:10]
        
        for book in books :
            book.status='o'
            book.save()
            
        response= self.client.get(reverse("my-borrowed"))
        
        self.assertEqual(response.context['user'],'testuser1')
        self.assertEqual(response.status_code,200)
        
        self.assertTrue("bookinstance_list" in response.context)
        for bookitem in response.context["bookinstance_list"] :
            self.assertEqual(response.context["user"],bookitem.borrower)
            
            self.assertEqual(bookitem.status ,'o')
        
    def test_pages_orederd_by_due_date(self):
        # change all the books to be on loan
        for book in BookInstance.objects.all() :
            book.status='o'
            book.save()
            
        login = self.client.login(username='testuser1',password='1145Man11')
        response = self.client.get(reverse("my-borrowed"))
        
        self.assertEqual(response.contect['user'],'testuser1')
        self.assertEqual(response.status_code,200)
        
        # confirm that the items are displayed only by 10 due to pegination
        self.assertEqual(len(response.context['bookinstance_list']),2)
        
        last_date = 0
        for book in response.context["bookinstance_list"] :
            if last_date == 0 :
                last_date= book.due_back
            else :
                self.assertTrue(last_date <= book.due_back)
                last_date= book.due_back
        
import uuid
from django.test import TestCase
from django.contrib.auth.models import Permission,User

class RenewBookInstanceViewTest(TestCase) :
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1',password='1145Man11')
        test_user1.save()
        
        test_user2 = User.objects.create_user(username='testuser2',password='1145Man11')
        permission = Permission.objects.get(name='Set book as returned ')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        #create book
        test_author = Author.objects.create(
            first_name='Usman',
            last_name='Ashir'
        )
        test_genre= Genre.objects.create(name="Romance")
        test_language = Language.objects.create(name='Arabic')
        test_book = Book.objects.create(
            title="Militiry",
            summary="The miliotiry of the army",
            isbn="AASDFGHJ",
            author=test_author,
            language= test_language,
        )
        # join the genre as its many to many relation ship
        genre_object = Genre.objects.all()
        test_book.genre.set(genre_object)
        test_book.save()
        
        #create book instance
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self .test_bookinstance1 = BookInstance.objects.create(
            book= test_book,
            imprint = "i like the copy that i got for the first copy ",
            due_back = return_date,
            borrower = test_user1,
            status = "o"
        )
        self .test_bookinstance2 = BookInstance.objects.create(
            book= test_book,
            imprint = "i like the copy that i got for the second copy ",
            due_back = return_date,
            borrower = test_user2,
            status = "o"
        )
        
    def test_redirect_ifnot_loggedin(self) :
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code ,302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_forbidden_ifnot_logged_in_but_not_corrrect_permission(self) :
        login = self.client.login(username='tetsuser1',password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code ,403)
        
    def test_logged_in_with_permission_Borrowed_books(self):
        login = self.client.login(username="testuser2",password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code ,200)
        
    def test_loggedin_with_permission_another_users_borrowed_books(self):
        login= self.client.login(username="testuser2",password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code,200)
        
    def test_HTTP404_for_in_valid_book_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username="testuser2",password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":test_uid}))
        self.assertEqual(response.status_code,404)
        
    def test_uses_correct_template(self):
        login =  self.client.login(username='testuser2',password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code,200)
        
        self.assertTemplateUsed(response,"catalog/book_renew_librarian.html")

    def tets_renewal_date_hasinitially_3weeks_in_future(self):
        login = self.client.login(username='testuser2',password="1145Man11")
        response = self.client.get(reverse("renew-book-librarian",kwargs={"pk":self.self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code,200)
        
        date_3weeks_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'],date_3weeks_future)
        
    #tets now if renewal succeeed usung the post request
    def test_redirect_to_all_borrowed_book_list_on_succeeed(self):
        login = self.client.login(username='testuser2',password='1145Man11')
        Valid_date_in_furure = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian',kwargs={"pk":self.test_bookinstance2.pk}),{"renewal_date":Valid_date_in_furure})
        self.assertRedirects(response,reverse('all-borrowed'))    
        
    def test_form_invalid_renewal_date_in_past(self):
        login= self.client.login(username="testuser2",password="1145Man11")
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance1.pk}),{"renewal_date":date_in_past})
        self.assertEqual(response.status_code,200)
        self.assertFormError(response,"form","renewal_date","invalid date renewal in past")
        
    def test_form_invalid_date_renewal_in_future(self) :
        login = self.client.login(username='testuser2',password='1145Man11')
        invalid_date_in_furture = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse("renew-book-librarian",kwargs={"pk":self.test_bookinstance1.pk}),{"renewal_date":invalid_date_in_furture})
        self.assertEqual(response.status_code,200)
        
        self.assertFormError(response,'form','renewal_date','invalid date - renewal more that 4 weeks ahead')
        
