from Reader_Module.borrowFunctionality import get_available_books, get_user_borrowed_books

def get_recommendation_data(u_Id):
    available = get_available_books()
    borrowed = get_user_borrowed_books(u_Id)
    return available, borrowed
