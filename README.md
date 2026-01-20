# Research Waste in Total Knee Arthroplasty Studies
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18316656.svg)](https://doi.org/10.5281/zenodo.18316656)

This repository contains the data and Python scripts used to generate the results published in:

> **Research waste in total knee arthroplasty studies: an observational study on registered trials**
> *BMJ Open* (2026)
> Authors: Annabelle R. Iken, Michiel Schaap, Rudolf W. Poolman, Maaike G. J. Gademan

Using this repository, you can fully reproduce the results presented in the study.

## Overview

This project analyzes "research waste" by examining discrepancies in clinical trial registration and publication. It includes a custom tool to convert **ClinicalTrials.gov JSON files** into **SPSS SAV files**.

While designed for this specific study, the tool was tested with the included dataset and can likely be adapted for other applications with minor modifications.

### Included Data
As an example, this repository contains the JSON data used for the additional search mentioned in the publication.
* **Source:** ClinicalTrials.gov
* **Date Retrieved:** May 22, 2025
* **Search Terms:** "total knee arthroplasty", "knee replacement", "knee arthroplasty of the knee", "arthroplasty knee"

## Citation

If you use the data or Python scripts in this repository, please cite the original publication:

> Iken AR, Schaap M, Poolman RW, et al. Research waste in total knee arthroplasty studies: an observational study on registered trials. *BMJ Open* 2026;:1–13. doi: bmjopen-2024-092409

## Installation

### Option 1: Simple Download (No Git required)
1.  Click the green **<> Code** button at the top of this page.
2.  Select **Download ZIP**.
3.  Unzip the file to your desired folder.

### Option 2: Using Git
If you have `git` installed, run the following command in your terminal:

```bash
git clone [https://github.com/ariken-research/convert_clinical_trial_gov_to_spss](https://github.com/ariken-research/convert_clinical_trial_gov_to_spss)
