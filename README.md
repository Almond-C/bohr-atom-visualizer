# Atom Visualizer: A Python Simulation of Electron Configuration

#### Video Demo:  [Youtube](https://youtu.be/YSbyZOL9rv8)

#### Description:

This project, **Atom Visualizer**, is an interactive Python program that simulates the atomic structure of elements by visualizing their electron configurations. The program provides a dual-window graphical interface built with `pygame`, allowing users to select elements from a simplified periodic table and observe a dynamic orbital representation of electrons around the nucleus.

---

### Features:

- A **graphical periodic table** interface lets users choose elements by clicking or dragging a slider.
- A **real-time orbital visualizer** displays shells and electrons according to the Bohr model, with animated rotation and energy bar charts.
- Includes a **slider mechanism** for adjusting atomic numbers between 1 and 118.


---

### File Overview:

- **`project.py`**  
  This is the main program file and entry point of the application. It contains:
  - `main()` – starts both GUI windows using `multiprocessing`.
  - `calculate_configuration(atomic_number)` – calculates the number of electrons per shell using predefined shell capacities.
  - `table_window(queue)` – opens the periodic table UI window and handles interaction logic.
  - `visualizer_window(queue)` – visualizes the nucleus, orbiting electrons, and energy level bars based on atomic number input.
  - Additional helper functions like `total_electrons(config)` and `get_shell_label(index)` are included for testability.

- **`test_project.py`**  
  This file includes unit tests for the logic functions in `project.py`. It uses `pytest` to validate:
  - Accurate electron configuration computation
  - Shell labeling logic
  - Total electron counting for a given configuration

- **`elements_config.py`**  
  A dictionary defining simplified periodic table data. Each element includes its position in the table grid and its symbol. This file is imported into `project.py` for GUI rendering.

- **`requirements.txt`**  
  <!-- Lists all pip-installable dependencies required to run the project. Currently includes: -->
  - `pygame`

- **`README.md`**  
  The file you're reading now – a detailed documentation of the project.
