# m6A Site Prediction using Autoencoder-XGBoost

## Purpose
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

## Running the Software

### Input Requirements
[TODO]

### Execution Commands
```bash
# Navigate to the project directory
cd dsa4262-genomesight

# Run the script
python auto_encoder_xgboost.py
```

### Output
[TODO]

## Interpreting the Output
[TODO]

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