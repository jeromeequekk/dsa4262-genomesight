import json
import gzip
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, make_scorer

M6A_FILE_PATH = "./data/data.info.labelled"
DIRECT_RNA_SEQ_DATA_FILE_PATH = "./data/dataset0.json.gz"
XGBOOST_MODEL_SAVE_PATH = "xgboost_best_model.json"

def read_m6A_labels(m6a_file_path):
    m6a_df = pd.read_csv(m6a_file_path, sep=",")
    m6a_df.columns = ["gene_id", "transcript_id", "transcript_position", "label"]
    return m6a_df

def convert_nucleotide_to_index(nucleotide):
    nucleotide = nucleotide.lower()
    if nucleotide == "a":
        return 0
    elif nucleotide == "c":
        return 1
    elif nucleotide == "g":
        return 2
    elif nucleotide == "t":
        return 3
    
def read_direct_rna_seq_data(data_path):
    data = []
    with gzip.open(data_path, 'rt') as f:
        for line in f:
            line_data = json.loads(line)
            for transcript_id, position_data in line_data.items():
                for transcript_position, combined_nucleotides_data in position_data.items():
                    for combined_nucleotide, reads in combined_nucleotides_data.items():
                        nucleotide_1, nucleotide_2, nucleotide_3, nucleotide_4, nucleotide_5, nucleotide_6, nucleotide_7 = combined_nucleotide
                        nucleotide_1_idx, nucleotide_2_idx, nucleotide_3_idx, nucleotide_4_idx, nucleotide_5_idx, nucleotide_6_idx, nucleotide_7_idx = convert_nucleotide_to_index(nucleotide_1), convert_nucleotide_to_index(nucleotide_2), convert_nucleotide_to_index(nucleotide_3), convert_nucleotide_to_index(nucleotide_4), convert_nucleotide_to_index(nucleotide_5), convert_nucleotide_to_index(nucleotide_6), convert_nucleotide_to_index(nucleotide_7)
                        for read_idx, read in enumerate(reads):
                            data.append({
                                'transcript_id': transcript_id,
                                'transcript_position': int(transcript_position),
                                'combined_nucleotide': combined_nucleotide,
                                'nucleotide_1_index': nucleotide_1_idx,
                                'nucleotide_2_index': nucleotide_2_idx,
                                'nucleotide_3_index': nucleotide_3_idx,
                                'nucleotide_4_index': nucleotide_4_idx,
                                'nucleotide_5_index': nucleotide_5_idx,
                                'nucleotide_6_index': nucleotide_6_idx,
                                'nucleotide_7_index': nucleotide_7_idx,
                                'read_id': read_idx,
                                'x_1': read[0],
                                'x_2': read[1],
                                'x_3': read[2],
                                'x_4': read[3],
                                'x_5': read[4],
                                'x_6': read[5],
                                'x_7': read[6],
                                'x_8': read[7],
                                'x_9': read[8]
                            })
    df = pd.DataFrame(data)
    return df

m6a_labels_df = read_m6A_labels(M6A_FILE_PATH)
rna_seq_data_df = read_direct_rna_seq_data(DIRECT_RNA_SEQ_DATA_FILE_PATH)
rna_seq_data_with_labels_df = rna_seq_data_df.merge(m6a_labels_df, on=["transcript_id", "transcript_position"], how="left")
aggregated_df = rna_seq_data_df.drop(columns=['read_id']).groupby(['transcript_id', 'transcript_position', 'combined_nucleotide',
                                                                   'nucleotide_1_index', 'nucleotide_2_index', 'nucleotide_3_index',
                                                                   'nucleotide_4_index', 'nucleotide_5_index', 'nucleotide_6_index',
                                                                   'nucleotide_7_index']).quantile(0.25).reset_index()
aggregated_with_labels_df = aggregated_df.merge(m6a_labels_df, on=["transcript_id", "transcript_position"], how="left")

features = aggregated_with_labels_df[['nucleotide_1_index', 'nucleotide_2_index', 'nucleotide_3_index', 'nucleotide_4_index',
                                      'nucleotide_5_index', 'nucleotide_6_index', 'nucleotide_7_index', 'x_1', 'x_2', 'x_3',
                                      'x_4', 'x_5', 'x_6', 'x_7', 'x_8', 'x_9']]
labels = aggregated_with_labels_df['label']

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

xgb_clf = xgb.XGBClassifier(scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train))

param_grid = {
    'n_estimators': [100, 200, 300],     # Increased range for number of trees
    'max_depth': [3, 6, 9],                    # Expanded maximum tree depth
    'learning_rate': [0.01, 0.05, 0.1],   # Added lower learning rates
    'subsample': [0.7, 0.8, 1.0],           # Expanded subsampling rates
    'colsample_bytree': [0.5, 0.7, 1.0],    # Expanded range for column subsampling
    'gamma': [0, 0.1, 0.3],                 # Regularization term on tree splits
    'reg_alpha': [0, 0.1, 1],               # L1 regularization
    'reg_lambda': [1, 2, 5],                 # L2 regularization
    'min_child_weight': [1, 3, 5]               # Minimum sum of instance weight (hessian)
}

def combined_score(y_true, y_pred_proba, **kwargs):
    roc = roc_auc_score(y_true, y_pred_proba)
    pr = average_precision_score(y_true, y_pred_proba)
    return (roc + pr) / 2

custom_scorer = make_scorer(combined_score, needs_proba=True)

grid_search = GridSearchCV(
    estimator=xgb_clf,
    param_grid=param_grid,
    scoring=custom_scorer,
    cv=5,
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

best_model.save_model(XGBOOST_MODEL_SAVE_PATH)
print(f"XGBoost model saved to {XGBOOST_MODEL_SAVE_PATH}")

y_pred_proba = best_model.predict_proba(X_test)[:, 1]

roc_auc = roc_auc_score(y_test, y_pred_proba)
pr_auc = average_precision_score(y_test, y_pred_proba)

print(f"ROC-AUC: {roc_auc:.4f}")
print(f"PR-AUC: {pr_auc:.4f}")
