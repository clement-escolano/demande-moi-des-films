# coding: utf-8

from app.recommendation import Recommendation


class Bot(object):

    def __init__(self):
        self.recommendation = Recommendation()

    def respond_to(self, sender, message):
        # Enregistre l'utilisateur s'il n'existe pas déjà
        user = self.recommendation.register_user(sender)

        # Donne le message pour que l'utilisateur l'utilise
        user.give_message(message)

        # Si le chatbot doit faire une recommandation ou pas
        if user.should_make_recommendation():
            return self.recommendation.make_recommendation(user)
        else:
            intro = ""
            # Si l'utilisateur parle pour la première fois, affiche un message d'intro
            if not user.has_been_asked_a_question():
                intro = "Bonjour ! Je vais vous poser des questions puis vous faire une recommandation.\n"

            message = self.recommendation.ask_question(user)
            return intro + message
