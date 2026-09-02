from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from analysis import clean_data, create_question_figure, run_question


PROJECT_DIR = Path(__file__).resolve().parent
df = clean_data(pd.read_csv(PROJECT_DIR / "netflix_customer_churn.csv"))

assert df.shape == (5000, 14)
assert round(run_question(df, 1), 2) == 43.85
assert round(run_question(df, 2), 2) == 11.65
assert run_question(df, 4).index[0] == "Premium"
assert round(run_question(df, 19), 1) == 50.3
assert run_question(df, 30).index[0] == "Premium"

for question_number in range(1, 31):
    result = run_question(df, question_number)
    figure = create_question_figure(df, question_number, result)
    assert figure is not None
    plt.close(figure)

print("All 30 analyses passed.")
