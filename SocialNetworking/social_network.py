# Name: Scarlett Nguyen
# CSE 160
# Homework 5

import utils  # noqa: F401, do not remove if using a Mac
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


###
#  Problem 1a
###

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()

    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("B", "C")
    # (Your code for Problem 1a goes here.)
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("C", "D")
    practice_graph.add_edge("C", "F")
    practice_graph.add_edge("D", "F")
    practice_graph.add_edge("D", "E")

    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


###
#  Problem 1b
###

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    # (Your code for Problem 1b goes here.)
    rj.add_edge("Nurse", "Juliet")
    rj.add_edge("Juliet", "Tybalt")
    rj.add_edge("Juliet", "Capulet")
    rj.add_edge("Juliet", "Friar Laurence")
    rj.add_edge("Juliet", "Romeo")
    rj.add_edge("Tybalt", "Capulet")
    rj.add_edge("Capulet", "Escalus")
    rj.add_edge("Capulet", "Paris")
    rj.add_edge("Escalus", "Mercutio")
    rj.add_edge("Escalus", "Paris")
    rj.add_edge("Escalus", "Montague")
    rj.add_edge("Paris", "Mercutio")
    rj.add_edge("Mercutio", "Romeo")

    rj.add_edge("Romeo", "Montague")
    rj.add_edge("Romeo", "Benvolio")
    rj.add_edge("Romeo", "Friar Laurence")

    rj.add_edge("Benvolio", "Montague")

    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    fof_set = set()
    friends_list = friends(graph, user)
    for friend in friends_list:
        fof_set.update(friends(graph, friend))
    fof_set.remove(user)
    fof_set.difference_update(friends_list)
    return fof_set


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    return friends(graph, user1).intersection(friends(graph, user2))


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    dict = {}
    fof_set = friends_of_friends(graph, user)
    for friend in fof_set:
        dict[friend] = len(common_friends(graph, user, friend))
    return dict


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    list = []
    for key, value in map_with_number_vals.items():
        list.append([key, value])
    list = sorted(list, key=itemgetter(0))
    list = sorted(list, key=itemgetter(1), reverse=True)
    final_list = []
    for val in list:
        final_list.append(val[0])
    return final_list


def recommend_by_number_of_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    return number_map_to_sorted_list(number_of_common_friends_map(graph, user))


###
#  Problem 3
###

def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    dict = {}
    fof_set = friends_of_friends(graph, user)
    for friend in fof_set:
        cf_set = common_friends(graph, user, friend)
        dict[friend] = 0
        for friend_cf in cf_set:
            dict[friend] += 1 / len(friends(graph, friend_cf))
    return dict


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    return number_map_to_sorted_list(influence_map(graph, user))


###
#  Problem 5
###

def get_facebook_graph():
    """Builds and returns the facebook graph
    """
    fb_graph = nx.Graph()
    links_file = open("facebook-links.txt", "r")
    for line in links_file:
        line_split = line.split('\t')
        left = int(line_split[0])
        right = int(line_split[1])
        fb_graph.add_edge(left, right)
    return fb_graph


def main():
    # practice_graph = get_practice_graph()
    # Comment out this line after you have visually verified your practice
    # graph.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_practice_graph(practice_graph)

    rj = get_romeo_and_juliet_graph()
    # Comment out this line after you have visually verified your rj graph and
    # created your PDF file.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_rj(rj)

    ###
    #  Problem 4
    ###

    print("Problem 4:")

    # (Your Problem 4 code goes here.)
    list_same = []
    list_diff = []
    for node in rj.nodes:
        if recommend_by_number_of_common_friends(rj, node) == \
           recommend_by_influence(rj, node):
            list_same.append(node)
        else:
            list_diff.append(node)
    print("Unchanged Recommendations: ", sorted(list_same))
    print("Changed Recommendations: ",  sorted(list_diff))

    ###
    #  Problem 5
    ###
    facebook = get_facebook_graph()
    assert len(facebook.nodes()) == 63731
    assert len(facebook.edges()) == 817090

    ###
    #  Problem 6
    ###
    print()
    print("Problem 6:")
    print()

    friends_1000 = []
    for node in facebook.nodes:
        if node % 1000 == 0:
            friends_1000.append(node)
    friends_1000 = sorted(friends_1000)
    common_list = []
    for item in friends_1000:
        lst = recommend_by_number_of_common_friends(facebook, item)[0:10]
        common_list.append(lst)
        print(item, '(by number_of_common_friends):', lst)

    ###
    #  Problem 7
    ###
    print()
    print("Problem 7:")
    print()

    influence_list = []
    for item in friends_1000:
        lst = recommend_by_influence(facebook, item)[0:10]
        influence_list.append(lst)
        print(item, '(by influence):', lst)

    ###
    # Problem 8
    ###
    print()
    print("Problem 8:")
    print()

    same = 0
    diff = 0
    for i in range(len(friends_1000)):
        if sorted(common_list[i]) == sorted(influence_list[i]):
            same += 1
        else:
            diff += 1
    print("Same:", same)
    print("Different:", diff)


if __name__ == "__main__":
    main()

###
# Collaboration: None
# Write your answer here, as a comment (on lines starting with "#").
