# Dryland Stability Loss

This repository contains the code used to analyze long-term changes in vegetation variability across global drylands and to investigate the mechanisms driving these changes.

## The workflow includes:

1. Plot global dryland trends in vegetation greenness and its variability(LAIcv)  
2. Decomposing LAIcv into vegetation upper and lower tails (LAI_max and LAI_min as well as each percentile)  
3. Attributing variability to climate variability and ecosystem sensitivity  
4. Evaluating model performance against observations  



## 📂 Repository Structure
```
Dryland-Stability-Loss
│
├── Fig1.ipynb # Vegetation variability (CV) trends
├── Fig2.ipynb # Divergence of vegetation extremes
├── Fig3.ipynb # Driver attribution
├── Fig4.ipynb # Model–observation comparison
├── __Global__.py # Path configuration (REQUIRED to modify)
├── __init__.py # Package imports and shared utilities
```


## 📦 Data Availability

Due to the large size of the datasets, input data are not included in this repository.

All required datasets are available at:

👉 **Zenodo:** 
https://zenodo.org/records/21536424


### Data contents include:

- Long-term LAI datasets (e.g., GIMMS4g LAI, SNU LAI,GLOBMAP LAI)  
- Climate datasets (e.g., CRU)  
- Derived variables (e.g., detrended LAI, CV metrics)  
- DGVM outputs (e.g., TRENDYv13)  

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/zw15772/Dryland-Stability-Loss.git
cd Dryland-Stability-Loss
```

### 2. Configure project root path
Before running any scripts, you must modify the root directory.

Open:
```
__Global__.py
```

Locate:
```this_root = 'your_project_root_path'```

Replace with your local path, e.g.:
```this_root = '/Users/yourname/Dryland-Stability-Loss/'```
### 3. Install dependencies
Python version: 3.13.12

Install required packages:

```pip install lytools==0.0.138 xymap==0.0.10 statsmodels```
Estimate installation time:
```5 minutes```


## Workflow
Run the notebooks in the following order:
```Fig1.ipynb → Fig2.ipynb → Fig3.ipynb → Fig4.ipynb```

Estimated runtime for each notebook:
```1-2 minutes```
