# coding: utf-8

from recommendation import Recommendation


class Bot(object):

    def __init__(self):
        self.recommendation = Recommendation()

    def respond_to(self, sender, message):
        user = self.recommendation.register_user(sender)
        user.answer_question(message)

        if user.should_make_recommendation():
            return self.recommendation.make_recommendation(user)
        else:
            intro = ""
            if not user.has_been_asked_a_question():
                intro = "Bonjour ! Je vais vous poser des questions puis vous faire une recommandation.\n"

            message, options = self.recommendation.ask_question(user)
            return intro + message, options
