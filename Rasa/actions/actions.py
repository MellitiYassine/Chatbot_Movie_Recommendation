# This file contains your custom actions which can be used to run custom Python code.
# See this guide on how to implement these action: https://rasa.com/docs/rasa/custom-actions

from typing import Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions import movie_functions as mf
import numpy as np


rmo = mf.rated_movies_org
rm = mf.rated_movies


class ActionActorVerification(Action):

    def name(self) -> Text:
        return 'action_actor_verification'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        actor = tracker.get_slot('actor')
        suggested = mf.is_this_your_person(actor)
        person_1 = suggested[0][0]
        dispatcher.utter_message("You mean, {}, right?".format(person_1))
        return []


class ActionActorVerificationPart2(Action):

    def name(self) -> Text:
        return 'action_actor_verification_2'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        actor = tracker.get_slot('actor')
        suggested = mf.is_this_your_person(actor)
        person_2 = suggested[1][0]
        dispatcher.utter_message("So did you mean, {}?".format(person_2))
        return []


class ActionSearchMovieActor(Action):

    def name(self) -> Text:
        return "action_search_with_actor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        actor = tracker.get_slot('actor')
        suggested = mf.is_this_your_person(actor)
        person_1 = suggested[0][0]
        result_1 = mf.find_movies_by_actor(person_1)
        dispatcher.utter_message("{} acted the following films: {}".format(person_1, result_1))
        return []


class ActionSearchMovieActorPart2(Action):

    def name(self) -> Text:
        return "action_search_with_actor_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        actor = tracker.get_slot('actor')
        suggested = mf.is_this_your_person(actor)
        person_2 = suggested[1][0]
        result_2 = mf.find_movies_by_actor(person_2)
        dispatcher.utter_message("{} acted the following films: {}".format(person_2, result_2))
        return []


class ActionDirectorVerification(Action):

    def name(self) -> Text:
        return 'action_director_verification'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        suggested = mf.is_this_your_person(director)
        person_1 = suggested[0][0]
        dispatcher.utter_message("You mean, {}, right?".format(person_1))
        return []


class ActionDirectorVerificationPart2(Action):

    def name(self) -> Text:
        return 'action_director_verification_2'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        suggested = mf.is_this_your_person(director)
        person_2 = suggested[1][0]
        dispatcher.utter_message("So did you mean, {}?".format(person_2))
        return []


class ActionSearchMovieDirector(Action):

    def name(self) -> Text:
        return "action_search_by_director"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        suggested = mf.is_this_your_person(director)
        person_1 = suggested[0][0]
        result_1 = mf.find_movies_by_director(person_1)
        dispatcher.utter_message("{} directed the following films: {}".format(person_1, result_1))
        return []


class ActionSearchMovieDirectorPart2(Action):

    def name(self) -> Text:
        return "action_search_by_director_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        suggested = mf.is_this_your_person(director)
        person_2 = suggested[1][0]
        result_2 = mf.find_movies_by_director(person_2)
        dispatcher.utter_message("{} directed the following films: {}".format(person_2, result_2))
        return []


class ActionMovieVerification(Action):

    def name(self) -> Text:
        return "action_movie_verification"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_1 = suggested[0][0]
        dispatcher.utter_message("{}, correct?".format(movie_1))
        return []


class ActionMovieVerificationPart2(Action):

    def name(self) -> Text:
        return "action_movie_verification_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_2 = suggested[1][0]
        dispatcher.utter_message(" Is {} the right movie?".format(movie_2))
        return []


class ActionSearchMovieData(Action):

    def name(self) -> Text:
        return "action_movie_data_lookup"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_1 = suggested[0][0]
        movie_df_len = mf.number_of_titles(movie_1)
        intent = tracker.get_intent_of_latest_message()
        if intent == 'affirm':
            if movie_df_len == 1:
                movie = mf.process_movie(movie_1)
                dispatcher.utter_message("Here is what I could find on {}".format(movie_1))
                dispatcher.utter_message(movie)
            else:
                result_other = mf.list_o_movies(movie_1)
                dispatcher.utter_message("There are multiple movies by that name. "
                                         "Here are your choices to narrow it down:")
                dispatcher.utter_message(result_other)
                dispatcher.utter_message('What year did the movie come out that you are looking for?')
        return []


class ActionSearchMovieDataPart2(Action):

    def name(self) -> Text:
        return "action_movie_data_lookup_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_2 = suggested[1][0]
        movie_df_len = mf.number_of_titles(movie_2)
        intent = tracker.get_intent_of_latest_message()
        if intent == 'affirm':
            if movie_df_len == 1:
                movie = mf.process_movie(movie_2)
                dispatcher.utter_message("Here is what I could find on {}".format(movie_2))
                dispatcher.utter_message(movie)
            else:
                result_other = mf.list_o_movies(movie_2)
                dispatcher.utter_message("There are multiple movies by that name. "
                                         "Here are your choices to narrow it down:")
                dispatcher.utter_message(result_other)
                dispatcher.utter_message('What year did the movie come out that you are looking for?')
        return []


class ActionSearchMovieYear(Action):

    def name(self) -> Text:
        return "action_movie_data_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        year = tracker.get_slot('year')
        suggested = mf.is_this_your_movie(movie_title)
        movie_1 = suggested[0][0]
        result_1 = mf.process_movie_2(movie_1, year)
        dispatcher.utter_message("Here is what I found.")
        dispatcher.utter_message(result_1)
        return []


class ActionSearchMovieYearPart2(Action):

    def name(self) -> Text:
        return "action_movie_data_year_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        year = tracker.get_slot('year')
        suggested = mf.is_this_your_movie(movie_title)
        movie_2 = suggested[1][0]
        result_2 = mf.process_movie_2(movie_2, year)
        dispatcher.utter_message(
            "Who knew there where that many movies titled {}. Anyway, here is what I found.".format(movie_2))
        dispatcher.utter_message(result_2)
        return []


class ActionRecMovieByGenre(Action):

    def name(self) -> Text:
        return "action_rec_movie_by_genre"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        genre = tracker.get_slot('genre')
        genre_2 = tracker.get_slot('genre_2')
        genre_3 = tracker.get_slot('genre_3')
        genres = [genre, genre_2, genre_3]
        genres = list(filter(None, genres))
        genres_str = ', '.join(map(str, genres))
        dispatcher.utter_message("{} movies coming right up.".format(genres_str))
        recommendations = mf.rec_movie_by_genre(genres)
        dispatcher.utter_message("Here are my recommendations: {}".format(recommendations))
        return [SlotSet("genre", None), SlotSet("genre_2", None), SlotSet("genre_3", None)]


class ActionRecMovieByMovie(Action):

    def name(self) -> Text:
        return "action_rec_movie_by_movie"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_1 = suggested[0][0]
        intent = tracker.get_intent_of_latest_message()
        if intent == 'affirm':
            idx = mf.get_recommendations(movie_1)
            if idx.shape == ():
                rec_1 = mf.idx_check(idx)
                dispatcher.utter_message("Here are my recommendations based off {}.".format(movie_1))
                dispatcher.utter_message(rec_1)
            else:
                movie_rm = rm[rm.original_title == movie_title]
                dispatcher.utter_message('There are multiple movies by that name. Here are your choices:')
                dispatcher.utter_message(movie_rm[['original_title', 'year', 'director', 'description']])
                dispatcher.utter_message('What year did the movie come out that you are looking for?')
        return []


class ActionRecMovieByMoviePart2(Action):

    def name(self) -> Text:
        return "action_rec_movie_by_movie_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        suggested = mf.is_this_your_movie(movie_title)
        movie_2 = suggested[1][0]
        intent = tracker.get_intent_of_latest_message()
        if intent == 'affirm':
            idx = mf.get_recommendations(movie_2)
            if idx.shape == ():
                rec_2 = mf.idx_check(idx)
                dispatcher.utter_message("Here are my recommendations based off {}.".format(movie_2))
                dispatcher.utter_message(rec_2)
            else:
                movie_rm = rm[rm.original_title == movie_title]
                dispatcher.utter_message('There are multiple movies by that name. Here are your choices:')
                dispatcher.utter_message(movie_rm[['original_title', 'year', 'director', 'description']])
                dispatcher.utter_message('What year did the movie come out that you are looking for?')
        return []


class ActionSearchMovieYearRec(Action):

    def name(self) -> Text:
        return "action_movie_rec_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        year = tracker.get_slot('year')
        suggested = mf.is_this_your_movie(movie_title)
        movie_1 = suggested[0][0]
        movie_rm = rm[rm.original_title == movie_1]
        new_idx = movie_rm[movie_rm.year == year]
        new_idx = np.int64(int(str(new_idx.index.values).strip('[').strip(']')))
        result = mf.idx_check(new_idx, movie_1)
        dispatcher.utter_message(
            "Who knew there where that many movies titled {}. Anyway, here is what I found.".format(movie_1))
        dispatcher.utter_message(result)
        return []


class ActionSearchMovieYearRecPart2(Action):

    def name(self) -> Text:
        return "action_movie_rec_year_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        movie_title = tracker.get_slot('movie_title')
        year = tracker.get_slot('year')
        suggested = mf.is_this_your_movie(movie_title)
        movie_2 = suggested[1][0]
        movie_rm = rm[rm.original_title == movie_2]
        new_idx = movie_rm[movie_rm.year == year]
        new_idx = np.int64(int(str(new_idx.index.values).strip('[').strip(']')))
        result = mf.idx_check(new_idx, movie_2)
        dispatcher.utter_message(
            "Who knew there where that many movies titled {}. Anyway, here is what I found.".format(movie_2))
        dispatcher.utter_message(result)
        return []
