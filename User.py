class User:

    def __init__(self, sender_id):
        self.id = sender_id
        # Variables utilisées pour suivre l'évolution de l'utilisateur
        self.latest_movie_asked = None
        self.questions_before_recommendation = None
        # Variables utilisées pour le premier algorithme
        self.good_ratings = []
        self.bad_ratings = []
        self.neutral_ratings = []
        # Variables utilisées pour le deuxième algorithme
        self.ratings = dict()

    def has_been_asked_a_question(self):
        return self.latest_movie_asked is not None

    # Si l'utilisateur a répondu oui
    def answer_yes(self):
        self.good_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    # Si l'utilisateur a répondu non
    def answer_no(self):
        self.bad_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    # Si l'utilisateur a répondu autre chose
    def answer_neutral(self):
        self.neutral_ratings.append(self.latest_movie_asked)

    # Détermine si l'utilisateur a répondu à suffisamment de questions pour lui faire une recommandation.
    def should_make_recommendation(self):
        if self.questions_before_recommendation is None:
            return False
        return self.questions_before_recommendation <= 0

    # Enregistre le film qu'on a demandé à l'utilisateur pour le traiter au prochain message
    def set_question(self, movie_number):
        self.latest_movie_asked = movie_number
        if self.questions_before_recommendation is None or self.questions_before_recommendation <= 0:
            self.questions_before_recommendation = 5

    # Traite le message de l'utilisateur
    def give_message(self, message):
        # Si on a rien demandé à l'utilisateur alors on ne fait rien
        if self.latest_movie_asked is None:
            return

        # On enlève les espaces en trop et on met tout le message en miniscule
        clean_message = message.lower().strip()

        # Il faut traiter ici le message
        return

    # Donne la norme de l'utilisateur
    def get_norm(self):
        return 1

    # Donne un vecteur avec les notations normalisées de l'utilisateur
    def get_normalised_cluster_notations(self):
        return []
