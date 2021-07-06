from deepevolution import wrap_keras
import pandas as pd
import matplotlib.pyplot as plt
from model import get_model,get_model2
from evaluate import evaluate_snek


model = get_model()
model.compile()


evaluate_snek(model)
