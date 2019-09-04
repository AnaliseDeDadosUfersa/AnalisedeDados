from sklearn.ensemble import AdaBoostClassifier
from CommonModel import CommonModel

class AdaBoost (CommonModel):
    def __init__(self, link, positionTarget, language = "en"):
        super().__init__(link, positionTarget, AdaBoostClassifier(n_estimators=100, random_state=0), language) 