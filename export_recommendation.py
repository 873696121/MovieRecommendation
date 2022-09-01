import numpy as np
import random
import math
from operator import itemgetter


class AppletRecommend():
    # initialize
    def __init__(self):
        # 找到与目标用户兴趣相似的5个用户，为其推荐4部电影
        self.n_sim_user = 5
        self.n_rec_applet = 4

        self.appletSet = {}
        self.profileSet = {}

        self.appletNum = 0
        self.userNum = 0
        self.profileNum = 0

        # 用户相似度矩阵
        self.user_sim_applet_matrix = {}
        self.user_sim_profile_matrix = {}

    def load_file(self, filename):
        with open(filename, 'r', encoding='utf8') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')

    def get_dataset(self, applet_filename, profile_filename):
        for line in self.load_file(applet_filename):
            user, applet, rating, time = line.split(',')
            self.appletNum = max(self.appletNum, int(applet) + 1)
            self.userNum = max(self.userNum, int(user) + 1)
            self.appletSet.setdefault(user, {})
            self.appletSet[user][applet] = rating
        for line in self.load_file(profile_filename):
            user, profile, rating, time = line.split(',')
            self.userNum = max(self.userNum, int(user) + 1)
            self.profileNum = max(self.profileNum, int(profile) + 1)
            self.profileSet.setdefault(user, {})
            self.profileSet[user][profile] = rating
        print('%d %d %d' % (self.userNum, self.appletNum, self.profileNum))

    def get_cos_similar(self, v1: list, v2: list):
        num = float(np.dot(v1, v2))  # 向量点乘
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)  # 求模长的乘积
        return 0.5 + 0.5 * (num / denom) if denom != 0 else 0

    def get_cos_similar_matrix(self, v1, v2):
        num = np.dot(v1, np.array(v2).T)  # 向量点乘
        denom = np.linalg.norm(v1, axis=1).reshape(-1, 1) * np.linalg.norm(v2, axis=1)  # 求模长的乘积
        res = num / denom
        res[np.isneginf(res)] = 0
        return 0.5 + 0.5 * res

    def calc_user_sim_cosine(self):
        # user-applet-matrix
        user_applet_matrix = np.eye(self.userNum, self.appletNum)
        for user, applets in self.appletSet.items():
            for applet in applets:
                # print('%s %s %s'%(user, applet, self.appletSet[user][applet]))
                user_applet_matrix[int(user)][int(applet)] = float(self.appletSet[user][applet])

        res = self.user_sim_applet_matrix = self.get_cos_similar_matrix(user_applet_matrix, user_applet_matrix)
        print(res)

    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_applet

        # 找到其最相似的K个用户
        print(self.user_sim_applet_matrix[int(user)])

        rank = {}
        watched_movies = self.appletSet[user]
        print(watched_movies)

        # # v=similar user, wuv=similar factor
        # for v, wuv in sorted(self.user_sim_applet_matrix[int(user)].items(), key=itemgetter(1), reverse=True)[0:K]:
        #     for movie in self.appletSet[v]:
        #         if movie in watched_movies:
        #             continue
        #         rank.setdefault(movie, 0)
        #         rank[movie] += wuv
        # return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    def train(self):
        for user in self.appletSet.items():
            print(self.recommend(user[0]))
            break

    def run(self):
        applet_file = '/Users/huhong/workspace/PythonProjects/MovieRecommendation/ml-latest-small/ratings.csv'
        # applet_file = 'U:\\project\\applet_matrix.csv'
        # profile_file = '/Users/huhong/PycharmProjects/MovieRecommendation/ml-latest-small/ratings.csv'
        # profile_file = 'U:\\project\\profile_matrix.csv'
        appletRecommend = AppletRecommend()
        appletRecommend.get_dataset(applet_file, applet_file)
        appletRecommend.calc_user_sim_cosine()


if __name__ == '__main__':
    A = AppletRecommend()
    A.run()
