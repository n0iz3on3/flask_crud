import atexit

from errors import HttpError, error_handler
from models import close_db, init_db
from views import UserView, AdsView, login, register

from app import get_app

init_db()
atexit.register(close_db)

app = get_app()

app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule(
    "/users/<int:user_id>",
    view_func=UserView.as_view("user"),
    methods=["GET", "PATCH", "DELETE"],
)
app.add_url_rule(
    "/ads/<int:ads_id>",
    view_func=AdsView.as_view("ads"),
    methods=["GET", "PATCH", "DELETE"],
)
app.add_url_rule(
    "/ads", view_func=AdsView.as_view("ads_create"), methods=["POST"]
)

app.errorhandler(HttpError)(error_handler)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000)
