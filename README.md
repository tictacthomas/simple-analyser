# Sensor Data Analyzer 

A Python project for analyzing and visualizing simulated offshore sensor data.

## Result folder
if you are just interested in the result of the script and do not want to run it yourself. 
the result folder has the generated data that the script provides.

## Technologies used
- Python 3.10+
- pandas
- matplotlib
- plotly

## How to run

### 1. Install dependencies
```bash
pip install pandas matplotlib plotly
```

### 2. Run the analyzer
```bash
python analyzer.py
```


## Project structure
```
simple_analyzer/
├── analyzer.py       # Main script – clean, analyze, visualize
├── generate_data.py  # Generates simulated sensor data
└── README.md
```

## Output
- `sensor_report.png` – static graph, open in any image viewer
- `sensor_dashboard.html` – interactive dashboard, open in browser
- you can ignore the generated __pycache__ folder
