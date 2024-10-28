# m6A Site Prediction using Autoencoder-XGBoost [TODO]

## Purpose
[TODO]
This software combines an autoencoder neural network with XGBoost to predict m6A modification sites in RNA sequences using direct RNA sequencing data. The model first uses an autoencoder to learn compressed representations of the nucleotide and signal features, then employs XGBoost for the final classification of modification sites.

## Getting Started (for Research Gateway Users)

### 1. Set Up AWS EC2 Instance
1. Launch an EC2 instance with the following specifications:
   1. **Product Name**: Create a suitable product name
   2. **KeyPair**: Create a pem key if you do not already have one
   3. **EBS Volume Size**: Attach at least 100GB EBS volume
   4. **Instance Type**: Select t3.large or better instance type

2. Connect to your instance (via SSH):
   1. **Username**: `Ubuntu`
   2. **Select Authentication Type**: `Pem File`
   3. **Pem File**: Select your Pem File here

### 2. Install Development Tools
```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python and development tools
sudo apt install python3-pip python3-dev gcc g++ make git -y

# Upgrade pip
python3 -m pip install --upgrade pip
```

### 3. Install the Software
```bash
# Clone the repository
git clone https://github.com/jeromeequekk/dsa4262-genomesight.git
cd dsa4262-genomesight

# Install required Python packages from requirements.txt
pip install -r requirements.txt

# Create data directory
mkdir data
```


### 4. Downloading the data (Optional if you already have your data)
These commands download from SG-NEx dataset, and copies these data into the `data/` folder

#### 1. Either from `xpore`
```bash
# A549: lung carcinoma epithelial cell line
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_A549_directRNA_replicate5_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_A549_directRNA_replicate6_run1/data.json data/

# Hct116: colon cancer cells
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_Hct116_directRNA_replicate3_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_Hct116_directRNA_replicate3_run4/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_Hct116_directRNA_replicate4_run3/data.json data/

# HepG2: human liver cancer cell line
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_HepG2_directRNA_replicate5_run2/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_HepG2_directRNA_replicate6_run1/data.json data/

# K562: lymphoblast cells isolated from the bone marrow of a 53-year-old chronic myelogenous leukemia patient
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_K562_directRNA_replicate4_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_K562_directRNA_replicate5_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_K562_directRNA_replicate6_run1/data.json data/

# MCF7: breast cancer cell line isolated in 1970 from a 69-year-old White woman
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_MCF7_directRNA_replicate3_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/xpore/SGNex_MCF7_directRNA_replicate4_run1/data.json data/
```

#### 2. Or from `m6Anet`
```bash
# A549: lung carcinoma epithelial cell line
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_A549_directRNA_replicate5_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_A549_directRNA_replicate6_run1/data.json data/

# Hct116: colon cancer cells
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_Hct116_directRNA_replicate3_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_Hct116_directRNA_replicate3_run4/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_Hct116_directRNA_replicate4_run3/data.json data/

# HepG2: human liver cancer cell line
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_HepG2_directRNA_replicate5_run2/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_HepG2_directRNA_replicate6_run1/data.json data/

# K562: lymphoblast cells isolated from the bone marrow of a 53-year-old chronic myelogenous leukemia patient
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_K562_directRNA_replicate4_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_K562_directRNA_replicate5_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_K562_directRNA_replicate6_run1/data.json data/

# MCF7: breast cancer cell line isolated in 1970 from a 69-year-old White woman
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_MCF7_directRNA_replicate3_run1/data.json data/
aws s3 cp --no-sign-request s3://sg-nex-data/data/processed_data/m6Anet/SGNex_MCF7_directRNA_replicate4_run1/data.json data/
```

Please refer to the following [link](https://github.com/GoekeLab/sg-nex-data/blob/master/docs/AWS_data_access_tutorial.md#processed-data), if you have trouble access or downloading the SG-NEx dataset

## Running the Software

### Input Requirements
The script expects the input files in the ./data/ directory:
Either:
1. Gzipped JSON file containing direct RNA sequencing data
Or: 
2. JSON file containing direct RNA sequencing data

### Execution Commands
```bash
# Navigate to the project directory
cd dsa4262-genomesight

# Run the script
python auto_encoder_xgboost.py
```

### Output
The script generates a CSV file containing:
- transcript_id
- transcript_position
- score (prediction probability for m6A modification)


## Interpreting the Output
- The output CSV contains prediction scores between 0 and 1
- Higher scores (closer to 1) indicate higher confidence of m6A modification
- Scores closer to 0 indicate lower likelihood of modification

## Script Arguments and Configuration
[TODO]

## Contributors
* [Jiang Ruirong](https://github.com/ruironggg)
* [Quek Yan Jun, Jerome](https://github.com/jeromeequekk)
* [Tan Wan Ting Andy](https://github.com/mujidan)
* [Pek Zi Wei, Zenden](https://github.com/zendenpek)


## How to Cite
If you use this software in your research, please cite:
```
Jiang Ruirong, Quek Yan Jun Jerome, Tan Wan Ting Andy, Pek Zi Wei Zenden. (2024). dsa4262-genomesight. https://github.com/jeromeequekk/dsa4262-genomesight
```