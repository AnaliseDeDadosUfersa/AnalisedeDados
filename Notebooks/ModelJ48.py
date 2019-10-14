from CommonModel import CommonModel
from sklearn.tree import DecisionTreeClassifier

class ModelJ48(CommonModel):
    def __init__(self, link, positionTarget, language = "en"):
        super().__init__(link, positionTarget, DecisionTreeClassifier(criterion = "entropy", random_state = 100, max_depth=3, min_samples_leaf=5), language)