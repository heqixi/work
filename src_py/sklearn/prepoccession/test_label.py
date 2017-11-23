import numpy as np 
from .label import LabelEncoder
myEncoder = LabelEncoder()
test_ar = ['0heqixi','tangxianmai','liuwaman']
fitted_label = myEncoder.fit(test_ar)
print(fitted_label)
labeled_test = myEncoder.transfrom(test_ar)
print(labeled_test)
