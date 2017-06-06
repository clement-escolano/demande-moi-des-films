class User:

    def __init__(self, sender_id):
        self.id = sender_id
        self.good_ratings = []
        self.bad_ratings = []
        self.latest_movie_asked = None
        self.questions_before_recommendation = None

    def answer_yes(self):
        self.good_ratings.append(self.latest_movie_asked)
        self.latest_movie_asked = None
        self.questions_before_recommendation -= 1

    def answer_no(self):
        self.bad_ratings.append(self.latest_movie_asked)
        self.latest_movie_asked = None
        self.questions_before_recommendation -= 1
