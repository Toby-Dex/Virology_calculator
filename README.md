# 🦠 Viral Titer Calculator

A comprehensive Streamlit web application for virology researchers to calculate viral titer and plan experiments well.

## Live Demo
**Try it here:** [Viral Titer Calculator](https://titer-my-virus.streamlit.app/)

---

## Features

### PFU Titer Calculator
- **Quick PFU/mL Calculation**: Automatically calculates plaque-forming units per milliliter
- **Countability Warnings**: Alerts when plaque counts fall outside optimal range (30-300)
- **Customizable Experimental Details**: Cell line, incubation time, plate type, overlay medium
- **Auto-generated Methods Section**
- **PDF Report Generation**: Download professional reports with all calculation details

### Stock Dilution Calculator
- **Reverse Calculator**: Calculate volume needed to achieve target PFU amount
- **Smart Dilution Suggestions**: Recommendations for pipetting accuracy
- **Practical Tips**: Guidance for small or large volume handling
- **Detailed Calculations**: Step-by-step breakdown of all computations

### TCID50 Calculator
- **Reed-Muench Method**: Most common TCID50 calculation method
- **Spearman-Karber Method**: Alternative method for incomplete data
- **Dynamic Dilution Input**: Flexible table for any number of dilutions (3-10)
- **Automatic Validation**: Checks for proper 50% endpoint transitions
- **TCID50 to PFU Conversion**: Approximate PFU equivalent (0.7 conversion factor)
- **Data Summary Tables**: Clear presentation of dilution series data

###  Additional Features
- **🌙 Dark Mode**: Toggle between light and dark themes
- **📈 Calculation History**: Automatic tracking of all calculations with timestamps
- **📥 CSV Export**: Download complete calculation history
- **📄 PDF Reports**: Generate professional reports for all calculator types
- **💾 Session Persistence**: Maintains history during active session

---

##  Why Use This Toolkit?

Virology labs will benefit from:
-  **Elimination of arithmetic errors** in titer calculations
-  **Standardized reporting** across experiments and researchers
-  **Time savings** on every single assay
-  **Consistent methods documentation** for publications
-  **Experiment planning** with reverse calculators
-  **Professional reports** with one-click PDF generation
-  **Calculation tracking** for lab notebooks and records

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Local Setup

1. **Clone this repository:**
```bash
git clone https://github.com/Toby-Dex/virology_calculator.git
cd virology_calculator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
streamlit run app.py
```

4. The app will open in your default web browser at `http://localhost:8501`

---

## Usage

### PFU Titer Calculator

1. Navigate to the ** PFU Calculator** tab
2. Enter your assay data:
   - **Plaques Counted**: Number of plaques on your plate
   - **Dilution Factor**: Select from dropdown (10⁻¹ to 10⁻⁹)
   - **Volume Plated**: Volume in microliters (µL)
3. Fill in experimental details for methods section
4. Click **Calculate PFU/mL**
5. View results, copy titer, or download PDF report

**Example:**
- Input: 50 plaques, 10⁻⁶ dilution, 100 µL volume
- Output: **5.00 × 10⁸ PFU/mL**  Optimal plaque count

### Stock Dilution Calculator

1. Navigate to the ** Reverse Calculator** tab
2. Enter known values:
   - **Stock Titer**: Your virus stock concentration
   - **Target PFU**: Desired amount of virus
3. Click **Calculate Volume Needed**
4. Get volume recommendations and dilution suggestions

**Example:**
- Stock: 5.0 × 10⁸ PFU/mL
- Target: 1.0 × 10⁶ PFU
- Result: **2.00 µL** needed

### TCID50 Calculator

1. Navigate to the ** TCID50 Calculator** tab
2. Select calculation method (Reed-Muench or Spearman-Karber)
3. Enter number of dilutions tested
4. Fill in dilution series data:
   - Dilution factor for each row
   - Positive wells and total wells
5. Click **Calculate TCID50**
6. View TCID50/mL result and PFU equivalent
7. Download PDF report with complete data table

---

## How It Works

### PFU Calculation Formula
```
PFU/mL = (Plaques Counted × Dilution Factor) / Volume Plated (mL)
```

### Countability Guidelines
- **Optimal Range**: 30-300 plaques
- **<30 plaques**: May lack statistical reliability
- **>300 plaques**: Plate may be too confluent for accurate counting

### TCID50 Calculation

**Reed-Muench Method:**
- Finds dilutions above and below 50% positive
- Calculates proportionate distance between them
- Determines TCID50 endpoint

**Spearman-Karber Method:**
```
TCID50 = 10^(x₀ - d(S - 0.5))
```
Where: x₀ = lowest dilution, d = dilution factor, S = sum of proportions

---

## Features in Detail

### Dark Mode
- Toggle in sidebar for comfortable viewing
- Persists during session
- Optimized for long calculation sessions

### Calculation History
- **Automatic Tracking**: All calculations saved with timestamps
- **Export to CSV**: Download complete history for lab records
- **Recent View**: Quick access to last 5 calculations
- **Clear Option**: Reset history when needed

### PDF Reports
- **Professional Formatting**: Publication-quality layout
- **Complete Data**: All inputs and parameters included
- **Methods Section**: Ready for manuscript submission
- **Timestamped**: Date and time of calculation

---

## Contributing

Contributions are welcome! If you have suggestions or find bugs:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tobi Lawal**
- Research Specialist, Emory University
- Emory Email: [Tlawal5@emory.edu](mailto:Tlawal5@emory.edu)
- Personal Email: [Tobilawal091@gmail.com](mailto:Tobilawal091@gmail.com)
- LinkedIn: [Lawal Tobi](https://www.linkedin.com/in/lawal-tobi-m-s-3247ab227)
- GitHub: [@Toby-Dex](https://github.com/Toby-Dex)

---

## Acknowledgments

Developed to streamline virology workflows and improve reproducibility in viral titer calculations. Special thanks to the virology research community for feedback and feature suggestions.

---

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{lawal2025virology,
  author = {Lawal, Tobi A.},
  title = {Viral Titer Toolkit},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Toby-Dex/virology_calculator}
}
```

Or in text:
```
Lawal, T.A. (2025). Viral Titer Toolkit. 
GitHub repository: https://github.com/Toby-Dex/virology_calculator
```

---

## Built With

- [Streamlit](https://streamlit.io/) - Web application framework
- [Python](https://www.python.org/) - Programming language
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [ReportLab](https://www.reportlab.com/) - PDF generation

---

## Bug Reports & Feature Requests

Found a bug or have a feature idea? Please [open an issue](https://github.com/Toby-Dex/virology_calculator/issues) on GitHub.

---

## Show Your Support

If this tool helped your research, please:
- ⭐ Star this repository
- 🔀 Fork it for your own modifications
- 📢 Share it with your lab and colleagues
- 📝 Cite it in your publications

---



