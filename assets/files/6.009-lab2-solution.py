import pickle

# NO OTHER IMPORTS ALLOWED!

BACON = 4724


def acted_together(data, actor_id_1, actor_id_2):
    """
    Returns True if the two given actors acted together (according to the given
    database) and False otherwise.
    """
    these_actors = {actor_id_1, actor_id_2}
    return any({i, j} == these_actors for i, j, _ in data)


def make_neighbor_db(data):
    """
    Returns a different mapping that is more conducive to the kinds of
    operations we want to perform.  This new mapping maps each actor id to a
    set of people they have acted with (these sets also contain IDs, not
    names).
    """
    acted_with = {}
    for i, j, _ in data:
        # the setdefault method lets us avoid checking for ourselves whether an
        # actor is already in the dictionary.
        # see https://docs.python.org/3/library/stdtypes.html#dict.setdefault
        acted_with.setdefault(i, set()).add(j)
        acted_with.setdefault(j, set()).add(i)
    return acted_with


def expand(acted_with, current_level, parents):
    """
    Run one "expansion", moving to a larger Bacon number.

    Arguments:
       acted_with: a mapping from IDs to the people they have acted with (the
                   output from make_neighbor_db)
       current_level: a set containing the IDs at the 'current' Bacon level (N)
       parents: a dictionary mapping actor IDs to their parents (i.e., the actor
                that led to them while traversing the graph).

    Returns:
       The set of people with Bacon number N+1
    """
    new_level = set()
    # We want to find all the neighbors of everyone at level N who have not
    # already been seen as we work outward from the center.
    for actor in current_level:
        for neighbor in acted_with[actor]:
            # Avoid duplicates by ignoring people we have already seen.  Every
            # actor we've seen is in the parents dictionary, so we skip any
            # actor that is already in that dictionary.
            if neighbor not in parents:
                # This is a new actor.  Add them to our set of people at level
                # N+1, and also add them to the parents dictionary so we don't
                # double-count them later.
                parents[neighbor] = actor
                new_level.add(neighbor)
    return new_level


def actors_with_bacon_number(data, n):
    """
    Returns the set of people who have a given Bacon number.
    """
    acted_with = make_neighbor_db(data)
    # Initialize the parents and the first level of the Bacon number (level 0).
    # BACON has no parent, and he is the only member of level 0.
    parents = {BACON: None}
    cur_level = {BACON}
    # Now, expand out N times, so that we end up with the people with Bacon
    # number N in cur_level.
    for i in range(n):
        cur_level = expand(acted_with, cur_level, parents)
        if not cur_level:
            return set()
    return cur_level  # Specification requires that we return a set.


def bacon_path(data, actor_id):
    """
    Returns the path of actor ids from BACON to the given actor ID.  Uses
    actor_to_actor_path.
    """
    return actor_to_actor_path(data, BACON, actor_id)


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """
    Return the path of actor IDs connecting actor_id_1 to actor_id_2
    """
    return actor_path(data, actor_id_1, lambda person: person == actor_id_2)


def actor_path(data, actor_id, goal_test):
    """
    Return the path of actor IDs connecting actor_id to the nearest person who
    satisfies the given goal test function.
    """
    # Create a more efficient structure to represent the connections between
    # actors.
    acted_with = make_neighbor_db(data)
    # Intialize the parents and the first level (starting from actor_id_1).
    # actor_id_1 is our root (it has no parent), and it is the only element in
    # the set of things that have 0 distance from itself.
    parents = {actor_id: None}
    cur_level = {actor_id}
    # Now we continually expand outward.  We stop in one of two conditions:
    # either someone in the current level satisfies the goal test (we
    # succeeded!) or there are no elements at the current level (we explored
    # the whole space and never found a match!).
    while cur_level:
        for person in cur_level:
            if goal_test(person):
                return trace_path(person, parents)
        cur_level = expand(acted_with, cur_level, parents)
    return None


def trace_path(person, parents):
    """
    Helper function for actor_to_actor_path.  This traces back through the parent
    dictionary from a given point and returns the path from the root to that
    point.
    """
    out = []
    while person is not None:
        out.append(person)
        person = parents[person]
    return out[::-1]  # the list we constructed is in reverse order, so flip it.


def get_actor_name_map():
    """
    Helper function for get_movie_path.  Returns a mapping from actor names to
    ID numbers.
    """
    with open('resources/names.pickle', 'rb') as f:
        return pickle.load(f)


def get_movie_name_map():
    """
    Helper function for get_movie_path.  Returns a mapping from movie names to
    ID numbers.
    """
    with open('resources/movies.pickle', 'rb') as f:
        return pickle.load(f)


def get_actors_to_movie_db(data):
    """
    Helper function for get_movie_path.  Returns a mapping from pairs of actors
    to the ID number of a movie in which they acted together.
    """
    out = {}
    for a1, a2, m in data:
        out[frozenset({a1, a2})] = m
    return out


def get_movie_to_actors_db(data):
    """
    Returns a mapping from movies to the set of actors who acted in the movie.
    """
    out = {}
    for a1, a2, m in data:
        out.setdefault(m, set()).update({a1, a2})
    return out


def actors_connecting_films(data, movie1, movie2):
    """
    Returns an actor path where the first actor acted in movie1, and the
    second actor acted in movie2. If no such path exists, returns None. 
    """
    movie_to_actors = get_movie_to_actors_db(data)
    paths_found = []
    try:
        paths = [actor_path(data, a, lambda b: b in movie_to_actors[movie2])
                        for a in movie_to_actors[movie1]]
        return min((path for path in paths if path is not None), key=len)
    except ValueError as e:
        # If we took the min of an empty sequence, meaning all paths were None, 
        # we got a ValueError--there is no path.
        return None


def get_movie_path(data, actor_name_1, actor_name_2):
    """
    Returns a list of movie names that connect the two given actors (here given
    as names, not as IDs)
    """
    # We start by creating a few useful mappings using the helper functions
    # above.
    movie_db = get_actors_to_movie_db(data)
    movie_name_db = {v: k for k,v in get_movie_name_map().items()}
    id_from_name = get_actor_name_map()
    # Next, determine the ID numbers of the given actors.
    actor_id_1 = id_from_name[actor_name_1]
    actor_id_2 = id_from_name[actor_name_2]
    # Find the path between them in terms of actors normally.
    actor_path = actor_to_actor_path(data, actor_id_1, actor_id_2)
    # Look up the movie ID numbers that connect each successive pair of actors.
    movie_id_path = [movie_db[frozenset(x)] for x in zip(actor_path, actor_path[1:])]
    # And, finally, convert the movie ID numbers into names.
    return [movie_name_db[i] for i in movie_id_path]


if __name__ == '__main__':
    with open('resources/large.pickle', 'rb') as f:
        largedb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass