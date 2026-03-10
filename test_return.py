import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

a = Analyzer()
df = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=100),
    'High': np.random.rand(100),
    'Low': np.random.rand(100),
    'Close': np.random.rand(100),
    'Volume': np.random.rand(100)
})

res = a.detect_flag_pattern(df)
print(f"RESULT TYPE: {type(res)}")
print(f"RESULT VALUE: {res}")

