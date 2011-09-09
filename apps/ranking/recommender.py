import stats

from models import *

MIN_SIMILARITY_VALUE = 0.25


class Recommender(object):
    
    def get_similar_users(self, user, user_list, item_list, limit=5, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        sim_list = []
        for other in user_list:
            if user==other:continue
            sim=distance_matrix_p1_p2(user_item_matrix[user.id],user_item_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
        
        sim_list.sort(reverse=True)
        return sim_list[:limit]
        
    
    def create_matrix(self, users, items):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Voto.objects.get_for_user_in_bulk(user)
            user_item_matrix[user.id] = votes_for_user

        return user_item_matrix


def distance_matrix_p1_p2(prefs_p1, prefs_p2):
    
    v1=[]
    v2=[]
    for item in prefs_p1:
        if item in prefs_p2:
            v1.append(prefs_p1[item].voto_int)
            v2.append(prefs_p2[item].voto_int)

    # if they have no ratings in common, return 0
    if len(v1)==0: return 0.0

    return pearson_correlation(v1,v2)
        

def pearson_correlation(v1,v2):

    try:
        pc= stats.pearsonr(v1,v2)[0]        
    except :
        pc= -1
    return (pc+1.0)/2.0