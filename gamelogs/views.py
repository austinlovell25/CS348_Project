from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import UserForm, ReviewForm
from .models import Publisher, Game, Review, User, Wishlist

from django.shortcuts import render
from .models import Review, Game, User


def select_dashboard(request):
    game_reviews = None
    avg_rating = None
    game_name = ''
    games = Game.objects.all()  # Retrieve all games for the dropdown
    publishers = Publisher.objects.all()  # Retrieve all publishers for the dropdown
    users = User.objects.all()  # Retrieve all users for the dropdown
    sort_option = "date_dsc"

    if request.method == 'POST':
        game_id = request.POST.get('game_id') or request.POST.get('game_select')
        publisher_id = request.POST.get('publisher_select')
        user_id = request.POST.get('user_select')
        sort_option = request.POST.get('sort_option')
        print(f"\n\nsort_option: {sort_option}")

        if sort_option == "date_asc":
            order_cls = "ORDER BY r.date;"
        elif sort_option == "date_dsc":
            order_cls = "ORDER BY r.date DESC;"
        elif sort_option == "rating_asc":
            order_cls = "ORDER BY r.rating;"
        elif sort_option == "rating_dsc":
            order_cls = "ORDER BY r.rating DESC;"
        else:
            order_cls = "ORDER BY r.date DESC;"


        # Use game_id to fetch reviews if provided
        if game_id:
            # SQL query to fetch reviews for the specified game ID
            query = """
                SELECT r.id, r.rating, r.date, u.username AS reviewer
                FROM gamelogs_review r
                JOIN gamelogs_user u ON r.user_id = u.id
                WHERE r.game_id = %s
                
            """
            query += order_cls
            game_reviews = Review.objects.raw(query, [game_id])

            query = """
                SELECT g.id, g.name
                FROM gamelogs_game g
                WHERE g.id = %s;
            """
            game_name = Review.objects.raw(query, [game_id])
            game_name = game_name[0].name

            # SQL query to fetch the average rating for the specified game ID
            avg_rating_query = """
                SELECT r.id, AVG(r.rating) AS avg_rating
                FROM gamelogs_review r
                WHERE r.game_id = %s;
            """
            avg_rating_result = Review.objects.raw(avg_rating_query, [game_id])
            avg_rating = avg_rating_result[0].avg_rating if avg_rating_result else None
            if avg_rating:
                avg_rating = round(avg_rating, 2)

        elif publisher_id:
            # Fetch reviews for games by the specified publisher
            query = """
                       SELECT r.id, r.rating, r.date, u.username AS reviewer
                       FROM gamelogs_review r
                       JOIN gamelogs_user u ON r.user_id = u.id
                       JOIN gamelogs_game g ON r.game_id = g.id
                       WHERE g.publisher_id = %s
                       
                   """
            query += order_cls
            game_reviews = Review.objects.raw(query, [publisher_id])

            query = """
                SELECT p.id, p.name
                FROM gamelogs_publisher p
                WHERE p.id = %s;
            """
            game_name = Review.objects.raw(query, [publisher_id])
            game_name = game_name[0].name

            # SQL query to fetch the average rating for the specified publisher
            avg_rating_query = """
                            SELECT r.id, AVG(r.rating) AS avg_rating
                            FROM gamelogs_review r
                            JOIN gamelogs_game g ON r.game_id = g.id
                            JOIN gamelogs_publisher p ON g.publisher_id = p.id
                            WHERE p.id = %s;
                        """
            avg_rating_result = Review.objects.raw(avg_rating_query, [publisher_id])
            avg_rating = avg_rating_result[0].avg_rating if avg_rating_result else None
            if avg_rating:
                avg_rating = round(avg_rating, 2)

        elif user_id:
            # Fetch reviews by the specified user
            query = """
                       SELECT r.id, r.rating, r.date, g.name AS game_name
                       FROM gamelogs_review r
                       JOIN gamelogs_game g ON r.game_id = g.id
                       WHERE r.user_id = %s
                       
                   """
            query += order_cls
            game_reviews = Review.objects.raw(query, [user_id])

            query = """
                SELECT u.id, u.username
                FROM gamelogs_user u
                WHERE u.id = %s;
            """
            game_name = Review.objects.raw(query, [user_id])
            game_name = game_name[0].username

            # SQL query to fetch the average rating for the specified user
            avg_rating_query = """
                SELECT r.id, AVG(r.rating) AS avg_rating
                FROM gamelogs_review r
                WHERE r.user_id = %s;
            """
            avg_rating_result = Review.objects.raw(avg_rating_query, [user_id])
            avg_rating = avg_rating_result[0].avg_rating if avg_rating_result else None
            if avg_rating:
                avg_rating = round(avg_rating, 2)

    return render(request, 'gamelogs/select_dashboard.html', {
        'game_reviews': game_reviews,
        'game_name': game_name,
        'avg_rating': avg_rating,
        'games': games,  # Pass the list of games to the template,
        'publishers': publishers,
        'users': users,
    })

def review_dashboard(request):
    # Get filter parameters from the request
    user_id = None
    users = User.objects.all()

    print(request.method)
    if 'user_id' in request.GET and request.GET['user_id'] and request.GET['user_id'] != "all":
        user_id = request.GET['user_id']
        print(user_id)
        query = """
            SELECT r.id, g.name, u.username, r.rating, r.date
            FROM gamelogs_review r
            JOIN gamelogs_user u ON r.user_id = u.id
            JOIN gamelogs_game g ON r.game_id = g.id
            WHERE u.id = %s
            ORDER BY r.date DESC;
        """
        filtered_reviews = Review.objects.raw(query, [user_id])

    else:
        query = """
            SELECT r.id, g.name, u.username, r.rating, r.date
            FROM gamelogs_review r
            JOIN gamelogs_user u ON r.user_id = u.id
            JOIN gamelogs_game g ON r.game_id = g.id
            ORDER BY r.date DESC;
        """
        filtered_reviews = Review.objects.raw(query)

    # Add context for rendering
    context = {
        'filtered_reviews': filtered_reviews,
        'users': users
    }
    return render(request, 'gamelogs/review_dashboard.html', context)


def index(request):
    return render(request, 'gamelogs/index.html')

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'gamelogs/add_user.html', {'form': form})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm()
    return render(request, 'gamelogs/add_review.html', {'form': form})

def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm(instance=review)
    return render(request, 'gamelogs/update_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        success_message = "Review successfully deleted."
        return render(request, 'gamelogs/delete_review.html', {'success_message': success_message})
    return render(request, 'gamelogs/delete_review.html', {'review': review})