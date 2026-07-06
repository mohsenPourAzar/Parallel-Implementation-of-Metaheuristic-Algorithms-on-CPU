# Parallel Implementation of Metaheuristic Algorithms on CPU

This project runs a **parallel Genetic Algorithm (GA)** experiment on CPU for the **CEC 2022 benchmark functions**. It uses [`mealpy`](https://pypi.org/project/mealpy/) for the GA implementation, [`opfunu`](https://pypi.org/project/opfunu/) for benchmark functions, and [`joblib`](https://pypi.org/project/joblib/) to execute multiple independent optimization runs in parallel.

The current implementation evaluates GA on:

- Dimensions: `10D` and `20D`
- Benchmark functions: `F1` to `F12` from CEC 2022
- Independent runs per benchmark: `30`
- Population size: `30`
- Maximum iterations: `1000`

For every benchmark function, the script prints summary statistics including mean, best, worst, median, and standard deviation.

---

## Project Structure

```text
.
├── main.py             # Main experiment script
├── README.md           # Project setup and usage guide
└── requirements.txt    # Required Python libraries
```

---

## Requirements

Use **Python 3.10 or newer**. The project requires the following Python libraries:

```text
numpy
mealpy
joblib
opfunu
```

These dependencies are also listed in `requirements.txt`.

---

## Setup and Installation

### 1. Extract or clone the project

Move into the project directory where `main.py` is located:

```bash
cd Parallel-Implementation-of-Metaheuristic-Algorithms-on-CPU-main
```

---

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal should show `(.venv)` at the beginning of the prompt.

---

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the main script:

```bash
python main.py
```

The script will start running the GA experiments and print progress similar to:

```text
Running GA_10D
{'Fn': 'F1', 'Mean': '...', 'Best': '...', 'Worst': '...', 'Median': '...', 'STD': '...'}
...
Running GA_20D
{'Fn': 'F1', 'Mean': '...', 'Best': '...', 'Worst': '...', 'Median': '...', 'STD': '...'}
...
```

---

## What the Script Does

The `main.py` file performs the following steps:

1. Defines the Genetic Algorithm settings:
   - `SearchAgents = 30`
   - `Max_iter = 1000`
   - `num_runs = 30`

2. Runs GA for two problem sizes:
   - `GA_10D`
   - `GA_20D`

3. Loads CEC 2022 benchmark functions from `opfunu`:
   - `F12022` to `F122022`

4. Executes `30` independent GA runs for each benchmark function.

5. Uses all available CPU cores through:

```python
Parallel(n_jobs=-1)
```

6. Collects and prints statistical results:
   - Mean fitness
   - Best fitness
   - Worst fitness
   - Median fitness
   - Standard deviation
   - Best position
   - Convergence curve

---

## Performance Notes

The default configuration is computationally expensive:

```python
2 dimensions × 12 benchmark functions × 30 runs × 1000 iterations
```

This can take a long time depending on your CPU. For a faster test run, reduce these values in `main.py`:

```python
SearchAgents = 10
Max_iter = 50
num_runs = 3
```

To limit CPU usage, change:

```python
Parallel(n_jobs=-1)
```

to a fixed number of workers, for example:

```python
Parallel(n_jobs=4)
```

`n_jobs=-1` uses all available CPU cores.

---

## Recommended First Test

Before running the full experiment, it is recommended to test the project with a smaller configuration:

```python
SearchAgents = 10
Max_iter = 50
num_runs = 3
```

Then run:

```bash
python main.py
```

If the script completes successfully, restore the full values for the final experiment.

---

## Output

The current version prints the results to the terminal. It does not automatically save results to a file.

The results are stored during runtime in this dictionary:

```python
statistics_all_benchmarks
```

Each benchmark entry contains:

```python
{
    "Fn": "F1",
    "Mean": "...",
    "Best": "...",
    "Worst": "...",
    "Median": "...",
    "STD": "...",
    "Best_position": [...],
    "Curve": [...],
    "Best_result": [...]
}
```

---

## Reproducibility Note

The current script does not set a random seed. Therefore, results may change between runs. If reproducible results are required, add a fixed seed before running the optimization logic.

Example:

```python
import numpy as np
np.random.seed(42)
```

Depending on the optimizer internals and multiprocessing behavior, additional seeding may be required for fully deterministic parallel experiments.

---

## Troubleshooting

### `ModuleNotFoundError`

If you see an error such as:

```text
ModuleNotFoundError: No module named 'mealpy'
```

make sure the virtual environment is active and install dependencies again:

```bash
pip install -r requirements.txt
```

---

### PowerShell activation error on Windows

If this command fails:

```powershell
.\.venv\Scripts\Activate.ps1
```

run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

### Very slow execution

The default experiment uses many independent runs and all CPU cores. Reduce these values for testing:

```python
SearchAgents = 10
Max_iter = 50
num_runs = 3
```

You can also limit CPU workers:

```python
Parallel(n_jobs=2)
```

---

## Main Dependencies

- `numpy`: numerical operations and statistical calculations
- `mealpy`: Genetic Algorithm optimizer
- `joblib`: parallel execution on CPU
- `opfunu`: CEC benchmark functions

---

## Suggested Future Improvements

The current version is functional, but these improvements are recommended for research-quality experiments:

1. Add command-line arguments for `SearchAgents`, `Max_iter`, `num_runs`, dimensions, and number of CPU workers.
2. Save results to `CSV`, `JSON`, or `Excel` instead of printing only to the terminal.
3. Save convergence curves for later plotting.
4. Add random seed control for reproducibility.
5. Add a `results/` directory for experiment outputs.
6. Add logging instead of plain `print` statements.

---

## Minimal Run Summary

```bash
cd Parallel-Implementation-of-Metaheuristic-Algorithms-on-CPU-main
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# or: .venv\Scripts\activate   # Windows CMD
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```
