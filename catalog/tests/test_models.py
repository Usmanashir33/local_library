from django.test import TestCase
from catalog.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="usman",last_name="ashir")
        
    def test_first_name_label(self):
        author =Author.objects.get(id=1)
        field_label=author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label,"first name")
        
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label=author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(field_label,"died")
        
    def test_first_name_max_length(self):
        author = Author .objects.get(id=1)
        max_length=author._meta.get_field("first_name").max_length
        self.assertEqual(max_length,100)
        
    def test_object_name_is_last_name_comma_first_name(self):
        author= Author.objects.get(id=1)
        expected_name = f"{author.last_name},{author.first_name}"
        self.assertEqual(str(author),expected_name)
        
    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(),"/catalog/author1")

from catalog.models import Language       
from django .test import TestCase
class LanguageModelTest(TestCase) :
    @classmethod
    def setUpTestData(cls) :
        Language.objects.create(name="Arabic")
        
    def test_field_label(self):
        language= Language.objects.get(id = 1)
        field_label = language._meta.get_field("name").verbose_name
        self.assertEqual(field_label,"Lang.")
        
    def test_field_max_length(self) :
        language = Language.objects.get(id = 1)
        max_length = language._meta.get_field("name").max_length
        self.assertEqual(max_length,50)
        
    def test_field_verbose_name_plural(self) :
        language= Language.objects.get(id=1)
        help_text = language._meta.verbose_name_plural
        self.assertEqual(help_text,"Languages")