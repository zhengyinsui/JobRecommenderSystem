import numpy as np
import pandas
#Class for Item similarity based Recommender System model
class item_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.UserID = None
        self.item_id = None
        self.cooccurence_matrix = None
        self.jobs_dict = None
        self.rev_jobs_dict = None
        self.item_similarity_recommendations = None

    #Create the item similarity based recommender system model
    def create(self, train_data, UserID, item_id):
        self.train_data = train_data
        self.UserID = UserID
        self.item_id = item_id

    #Get unique items (jobs) corresponding to a given user
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.UserID] == user]
        user_items = list(user_data[self.item_id].unique())

        return user_items

    #Get unique users for a given item (job)
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.UserID].unique())

        return item_users

    #Get unique items (jobs) in the training data
    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())

        return all_items

    #Construct cooccurence matrix
    def construct_cooccurence_matrix(self, user_jobs, all_jobs):

        ####################################
        #Get users for all jobs in user_jobs.
        ####################################
        user_jobs_users = []
        for i in range(0, len(user_jobs)):
            user_jobs_users.append(self.get_item_users(user_jobs[i]))

        ###############################################
        #Initialize the item cooccurence matrix of size
        #len(user_jobs) X len(jobs)
        ###############################################
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_jobs), len(all_jobs))), float)

        #############################################################
        #Calculate similarity between user jobs and all unique jobs
        #in the training data
        #############################################################
        for i in range(0,len(all_jobs)):
            #Calculate unique users of job i
            jobs_i_data = self.train_data[self.train_data[self.item_id] == all_jobs[i]]
            users_i = set(jobs_i_data[self.UserID].unique())

            for j in range(0,len(user_jobs)):

                #Get unique users of job j
                users_j = user_jobs_users[j]

                #Calculate intersection of users of jobs i and j
                users_intersection = users_i.intersection(users_j)

                #Calculate cooccurence_matrix[i,j] as Jaccard Index
                if len(users_intersection) != 0:
                    #Calculate union of users of jobs i and j
                    users_union = users_i.union(users_j)

                    cooccurence_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    cooccurence_matrix[j,i] = 0


        return cooccurence_matrix


    #Use the cooccurence matrix to make top recommendations
    def generate_top_recommendations(self, user, cooccurence_matrix, all_jobs, user_jobs):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(cooccurence_matrix))

        #Calculate a weighted average of the scores in cooccurence matrix for all user jobs.
        user_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()

        #Sort the indices of user_sim_scores based upon their value
        #Also maintain the corresponding score
        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)

        #Create a dataframe from the followingUserID
        columns = ['UserID', 'Job', 'score', 'rank']
        #index = np.arange(1) # array of numbers for the number of samples
        df = pandas.DataFrame(columns=columns)

        #Fill the dataframe with top 10 item based recommendations
        rank = 1
        for i in range(0,len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_jobs[sort_index[i][1]] not in user_jobs and rank <= 10:
                df.loc[len(df)]=[user,all_jobs[sort_index[i][1]],sort_index[i][0],rank]
                rank = rank+1

        #Handle the case where there are no recommendations
        if df.shape[0] == 0:
            print("The current user has no jobs for training the item similarity based recommendation model.")
            return -1
        else:
            return df



    #Use the item similarity based recommender system model to
    #make recommendations
    def recommend(self, user):

        ########################################
        #A. Get all unique jobs for this user
        ########################################
        user_jobs = self.get_user_items(user)

        print("No. of unique jobs for the user: %d" % len(user_jobs))

        ######################################################
        #B. Get all unique items (jobs) in the training data
        ######################################################
        all_jobs = self.get_all_items_train_data()

        print("no. of unique jobs in the training set: %d" % len(all_jobs))

        ###############################################
        #C. Construct item cooccurence matrix of size
        #len(user_jobs) X len(jobs)
        ###############################################
        cooccurence_matrix = self.construct_cooccurence_matrix(user_jobs, all_jobs)

        #######################################################
        #D. Use the cooccurence matrix to make recommendations
        #######################################################
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_jobs, user_jobs)

        return df_recommendations

    #Get similar items to given items
    def get_similar_items(self, item_list):

        user_jobs = item_list

        ######################################################
        #B. Get all unique items (jobs) in the training data
        ######################################################
        all_jobs = self.get_all_items_train_data()

        print("no. of unique jobs in the training set: %d" % len(all_jobs))

        ###############################################
        #C. Construct item cooccurence matrix of size
        #len(user_jobs) X len(jobs)
        ###############################################
        cooccurence_matrix = self.construct_cooccurence_matrix(user_jobs, all_jobs)

        #######################################################
        #D. Use the cooccurence matrix to make recommendations
        #######################################################
        user = ""
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_jobs, user_jobs)

        return df_recommendations
