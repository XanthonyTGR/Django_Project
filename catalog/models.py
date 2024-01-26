import uuid  # Required for unique book instances

from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. 'Science Fiction', 'French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Return the URL to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)


class Language(models.Model):
    """Model representing a language."""
    name = models.CharField(max_length=50, help_text="Enter the language name (e.g., 'English', 'French')")

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Return the URL to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book.")

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined, so we can specify the object above.
    genres = models.ManyToManyField(
        Genre,
        help_text="Select a genre for this book")
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Select the language of the book")

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Return the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e., that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library.")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = {
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    }
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text="Book availability"
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object"""
        return f' self(self.id ({self.book.title})'

    def display_info(self):
        """Create a string with book information for the BookInstance list view."""
        return f'{self.book.title}, Status: {self.get_status_display()}, Due Back: {self.due_back}, ID: {self.id}'

    def is_overdue(self):
        """Determines if the book is overdue based on the due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'