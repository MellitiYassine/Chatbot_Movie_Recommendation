import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

# load data
rated_movies_org = pd.read_csv(r"C:\Users\dougm\OneDrive\Bellevue\DSC680\Project 2\Data\rated_movies_org.csv.gz",
                               low_memory=False)
rated_movies = pd.read_csv(r"C:\Users\dougm\OneDrive\Bellevue\DSC680\Project 2\Data\rated_movies.csv.gz",
                           low_memory=False)
people = pd.read_csv(r"C:\Users\dougm\OneDrive\Bellevue\DSC680\Project 2\Data\people.csv.gz", low_memory=False)
roles = pd.read_csv(r"C:\Users\dougm\OneDrive\Bellevue\DSC680\Project 2\Data\roles.csv.gz", low_memory=False)
sim_feat = np.load(r"C:\Users\dougm\OneDrive\Bellevue\DSC680\Project 2\Data\cosine_sim_features.npy")
indices = pd.Series(rated_movies.index, index=rated_movies.original_title)


# function that recommends similar movies based of movie title input
def get_recommendations(title):
    if title in indices:
        # index of the movie that matches the title
        idx = indices[title]
        return idx


# idx check and recommend
def idx_check(idx, cosine_sim=sim_feat):
    # pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    # the top 5 most similar movies
    return ", ".join(list(rated_movies['original_title'].iloc[movie_indices]))


# to process movie info
def process_movie(title):
    movie = rated_movies_org[rated_movies_org.original_title == title]
    director = movie.iloc[0]['director']
    cast = movie.iloc[0]['actors']
    plot = movie.iloc[0]['description']
    genre = movie.iloc[0]['genre']
    released = movie.iloc[0]['year']
    imdb_rate = movie.iloc[0]['weighted_average_vote']
    q_vote = movie.iloc[0]['new_wav']
    return "Director: {}\n"\
           "Cast: {} \n"\
           "Plot: {} \n" \
           "Genre: {} \n"\
           "Released: {} \n"\
           "IMDb Rating: {} \n"\
           "Quentin's Rating: {}".format(director, cast, plot, genre, released, imdb_rate, q_vote)


# to process movie info
def process_movie_2(title, year):
    movie = rated_movies_org[(rated_movies_org.original_title == title) & (rated_movies_org.year == year)]
    director = movie.iloc[0]['director']
    cast = movie.iloc[0]['actors']
    plot = movie.iloc[0]['description']
    genre = movie.iloc[0]['genre']
    released = movie.iloc[0]['year']
    imdb_rate = movie.iloc[0]['weighted_average_vote']
    q_vote = movie.iloc[0]['new_wav']
    return "Director: {}\n"\
           "Cast: {} \n"\
           "Plot: {} \n" \
           "Genre: {} \n"\
           "Released: {} \n"\
           "IMDb Rating: {} \n"\
           "Quentin's Rating: {}".format(director, cast, plot, genre, released, imdb_rate, q_vote)


# too many movies to decide from
def list_o_movies(title):
    films = []
    movie = (rated_movies_org[rated_movies_org.original_title == title])
    for i in range(len(movie)):
        film = movie.iloc[i]['title', 'director', 'year']
        films.append(film)
    return ', '.join(str(i) for i in films)


# # of titles
def number_of_titles(title):
    num_titles = len(rated_movies_org[rated_movies_org.original_title == title])
    return num_titles


# find similar title
def is_this_your_movie(title):
    title1 = title
    title2 = rated_movies_org.original_title.to_list()
    scores = process.extract(title1, title2, scorer=fuzz.token_set_ratio)
    return scores


# find similar person
def is_this_your_person(person):
    person1 = person
    person2 = people.name.to_list()
    scores = process.extract(person1, person2, scorer=fuzz.token_set_ratio)
    return scores


# show me films with actor
def find_movies_by_actor(x):
    for i in range(len(people)):
        if people.name[i] == x:
            name_id = people.imdb_name_id[i]
    title_id = []
    for a in range(len(roles)):
        if (roles.imdb_name_id[a] in name_id) & ((roles.category[a] == 'actress') | (roles.category[a] == 'actor')):
            title_id.append(roles.imdb_title_id[a])
    list_of_films = rated_movies_org[rated_movies_org['imdb_title_id'].isin(title_id)]
    return ', '.join(str(i) for i in list_of_films.original_title)


# show me films by director
def find_movies_by_director(x):
    name_id = []
    for i in range(len(people)):
        if people.name[i] == x:
            name_id.append(people.imdb_name_id[i])
    title_id = []
    for d in range(len(roles)):
        if (roles.imdb_name_id[d] in name_id) & (roles.category[d] == 'director'):
            title_id.append(roles.imdb_title_id[d])
    list_of_films = rated_movies_org[rated_movies_org['imdb_title_id'].isin(title_id)]
    return ', '.join(str(i) for i in list_of_films.original_title)


# recommend movie by genre
def rec_movie_by_genre(x):
    movies_list = []
    for i in range(len(rated_movies)):
        if all(word in rated_movies.genre[i].lower() for word in x):
            movies_list.append([rated_movies.original_title[i], rated_movies.new_wav[i],
                                rated_movies.total_votes[i], rated_movies.year[i], rated_movies.director[i]])
            movies_list.sort(key=lambda y: (y[2], y[1]), reverse=True)
    movies_list = [movies_list[0][0], movies_list[1][0], movies_list[2][0]]
    movies_list = ', '.join(str(i) for i in movies_list)
    return movies_list
