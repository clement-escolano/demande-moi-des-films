# coding: utf-8

from recommendation import Recommendation


class Bot(object):

    def __init__(self):
        self.recommendation = Recommendation()

    def respond_to(self, sender, message):
        user = self.recommendation.register_user(sender)
        if not user.answer_question(message):
            message, options = self.recommendation.ask_question(user)
            message = "Bonjour ! Je vais vous poser des questions puis vous faire une recommandation" + message
            return message, options
        else:
            if user.should_make_recommendation():
                return self.recommendation.make_recommendation(user)
            else:
                return self.recommendation.ask_question(user)
