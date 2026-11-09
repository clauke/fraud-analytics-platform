from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)

# ============================================================
# Fraud Analytics Platform
# Sprint 6 - Machine Learning
# Analise de limiares - Random Forest
# ============================================================
