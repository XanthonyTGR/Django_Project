from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate count of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status ='a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.all().count()

    # Retrieve a list of BookInstance objects
    book_instances = BookInstance.objects.all()

    # Vist count
    num_authors_available = Author.objects.all().count()  # the 'all()' is implied by default

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'book_instances': book_instances,  # Add this line to pass the list to the template
        'num_visits': num_visits,
    }

    # Render  the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

