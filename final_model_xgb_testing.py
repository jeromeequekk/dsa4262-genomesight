import json
import gzip
import pandas as pd
import numpy as np
import xgboost as xgb

DIRECT_RNA_SEQ_DATA_FILE_PATH = "./data/dataset1.json.gz" # can use both .json or .json.gz
XGBOOST_MODEL_SAVE_PATH = "xgboost_best_model.json"
OUTPUT_CSV_PATH = "predictions_xgboost_dataset1.csv"

def read_direct_rna_seq_data(data_path):
    data = []
    if data_path.endswith(".gz"):
        f = gzip.open(data_path, 'rt')
    else:
        f = open(data_path, 'r')

    with f:
        for line in f:
            line_data = json.loads(line)
            for transcript_id, position_data in line_data.items():
                for transcript_position, combined_nucleotides_data in position_data.items():
                    for combined_nucleotide, reads in combined_nucleotides_data.items():
                        nucleotide_1, nucleotide_2, nucleotide_3, nucleotide_4, nucleotide_5, nucleotide_6, nucleotide_7 = combined_nucleotide
                        nucleotide_1_idx = convert_nucleotide_to_index(nucleotide_1)
                        nucleotide_2_idx = convert_nucleotide_to_index(nucleotide_2)
                        nucleotide_3_idx = convert_nucleotide_to_index(nucleotide_3)
                        nucleotide_4_idx = convert_nucleotide_to_index(nucleotide_4)
                        nucleotide_5_idx = convert_nucleotide_to_index(nucleotide_5)
                        nucleotide_6_idx = convert_nucleotide_to_index(nucleotide_6)
                        nucleotide_7_idx = convert_nucleotide_to_index(nucleotide_7)

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
                                'x_1': read[0], 'x_2': read[1], 'x_3': read[2],
                                'x_4': read[3], 'x_5': read[4], 'x_6': read[5],
                                'x_7': read[6], 'x_8': read[7], 'x_9': read[8]
                            })

    df = pd.DataFrame(data)
    return df

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

rna_seq_data_df = read_direct_rna_seq_data(DIRECT_RNA_SEQ_DATA_FILE_PATH)
aggregated_df = rna_seq_data_df.drop(columns=['read_id']).groupby(
    ['transcript_id', 'transcript_position', 'combined_nucleotide',
     'nucleotide_1_index', 'nucleotide_2_index', 'nucleotide_3_index',
     'nucleotide_4_index', 'nucleotide_5_index', 'nucleotide_6_index',
     'nucleotide_7_index']
).quantile(0.25).reset_index()

features = aggregated_df[
    ['nucleotide_1_index', 'nucleotide_2_index', 'nucleotide_3_index',
     'nucleotide_4_index', 'nucleotide_5_index', 'nucleotide_6_index',
     'nucleotide_7_index', 'x_1', 'x_2', 'x_3', 'x_4', 'x_5', 'x_6', 'x_7', 'x_8', 'x_9']
]

best_model = xgb.XGBClassifier()
best_model.load_model(XGBOOST_MODEL_SAVE_PATH)
print(f"XGBoost model loaded from {XGBOOST_MODEL_SAVE_PATH}")

y_prob = best_model.predict_proba(features)[:, 1]

results_df = aggregated_df[['transcript_id', 'transcript_position']].copy()
results_df['score'] = y_prob

results_df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"Predictions for the new dataset saved to {OUTPUT_CSV_PATH}")