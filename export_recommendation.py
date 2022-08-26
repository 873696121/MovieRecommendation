class AppletRecommend():
    # initialize
    def __init__(self):
        # 找到与目标用户兴趣相似的5个用户，为其推荐4部电影
        self.n_sim_user = 5
        self.n_rec_applet = 4

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        self.appletSet = {}
        self.profileSet = {}

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
            user, applet, rating = line.split(',')
            self.appletSet.setdefault(user, {})
            self.appletSet[user][applet] = rating
        for line in self.load_file(profile_filename):
            user, profile, rating = line.split(',')
            self.profileSet.setdefault(user, {})
            self.profileSet[user][profile] = rating

    def calc_user_sim(self):
        # 构建“电影-用户”倒排索引
        print("Building applet-user table ...")
        applet_user = {}
        for user, applets in self.appletSet.items():
            for applet in applets:
                if applet not in applet_user:
                    applet_user[applet] = set()
                applet_user[applet].add(user)
        profile_user = {}
        for user, profiles in self.profileSet.items():
            for profile in profiles:
                if profile not in profile_user:
                    profile_user[profile] = set()
                profile_user[profile].add(user)

        for applet, users in applet_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_applet_matrix.setdefault(u, {})
                    self.user_sim_applet_matrix[u].setdeault(v, 0)
                    self.user_sim_applet_matrix[u][v] += 1

        for profile, users in profile_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_profile_matrix.setdefault(u, {})
                    self.user_sim_profile_matrix[u].setdeault(v, 0)
                    self.user_sim_profile_matrix[u][v] += 1

    def run(self):
        applet_file = '/Users/huhong/PycharmProjects/MovieRecommendation/ml-latest-small/ratings.csv'
        # applet_file = 'U:\\project\\applet_matrix.csv'
        profile_file = '/Users/huhong/PycharmProjects/MovieRecommendation/ml-latest-small/ratings.csv'
        # profile_file = 'U:\\project\\profile_matrix.csv'
        appletRecommend = AppletRecommend()
        appletRecommend.get_dataset(applet_file, profile_file)


if __name__ == '__main__':
    AppletRecommend().run()
