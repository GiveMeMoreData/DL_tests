from deepevolution import wrap_keras
import pandas as pd
import matplotlib.pyplot as plt
from model import *
from evaluate import *

wrap_keras()


model = get_model_flat()
model.compile()


history = model.fit_evolve(X=None, Y=None, max_generations=500, population=50, top_k=20, mutation_rate=0.2, mutation_std=0.2, fitness_func=evaluate_positional_snek)


print(f"Model accuracy: {evaluate_positional_snek(model)}")
pd.DataFrame(history).plot()
plt.show()
