from CommonModel import CommonModel
from sklearn.neighbors import KNeighborsClassifier

class KNNModel(CommonModel):
    def __init__(self, link, positionTarget, language = "en"):
        super().__init__(link, positionTarget, KNeighborsClassifier(), language)
        



