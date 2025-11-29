# README
# Analytical Network Process (ANP) Script

This repository contains a fully integrated Python script implementing the Analytical Network Process (ANP). It includes modules for:

- **AHP weight calculation** (Geometric Mean, Arithmetic Mean, Eigenvector Methods)
- **Unweighted Supermatrix construction**
- **Weighted Supermatrix calculation**
- **Limit Supermatrix iteration** to obtain final priorities

## 📌 Requirements
Make sure you have the following Python libraries installed:
```bash
pip install numpy pandas xlrd
```

## 📁 Input Files Required
- `ANP_data1.xls` – Judgment matrices for the AHP section

## 🧩 Output Files Generated
- `001-ANP_result.xls` – AHP weight results
- `002-Supermatrix-Weight_Matrix.xls` – Unweighted supermatrix & cluster weight matrix
- `003-weighted_supermatrix.xls` – Weighted supermatrix
- `004-limit_supermatrix_result.xls` – Limit supermatrix (final ANP priorities)

## ▶️ How to Run
You can run the script and call functions manually:
```python
python your_script_name.py
```
Inside the Python environment:
```python
from your_script_name import AHP, unweighted_supermatrix, weighted_supermatrix, limit_supermatrix
AHP()
unweighted_supermatrix()
weighted_supermatrix()
limit_supermatrix()
```
