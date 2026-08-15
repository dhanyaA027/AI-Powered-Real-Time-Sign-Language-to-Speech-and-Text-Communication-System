import numpy as np
from features import landmarks_to_feature_vector
from sign_logic import SignLogic

class Point:
    def __init__(self,x,y,z=0): self.x,self.y,self.z=x,y,z

def test_feature_vector_shape():
    pts=[Point(.5+i*.001,.5+i*.001) for i in range(21)]
    assert landmarks_to_feature_vector(pts).shape==(63,)

def test_sign_logic_smoothing():
    logic=SignLogic(window=5,min_votes=3)
    assert logic.update("HELLO") is None
    assert logic.update("HELLO") is None
    assert logic.update("HELLO")=="HELLO"

def test_duplicate_suppression():
    logic=SignLogic(window=3,min_votes=2)
    assert logic.update("YES") is None
    assert logic.update("YES")=="YES"
    assert logic.update("YES") is None
