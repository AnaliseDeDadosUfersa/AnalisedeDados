from sklearn.neural_network import MLPClassifier as MLP
from CommonModel import CommonModel
class ModelMLP(CommonModel):
    def __init__(self, link, position):
        super().__init__(link, position, MLP())
