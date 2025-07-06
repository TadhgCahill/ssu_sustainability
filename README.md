## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Running](#running-the-program)

## About
Welcome to the SSU Sustainability repository! This web application utilizes the Dash Web Framework, Plotly for maps and graphs, and SQL for the backend.

## Getting Started
```
# create conda env
conda create --name conda_ssu_sustainability

# install packages
conda install -n conda_ssu_sustainability dash pandas pymysql

```
## Running the Program
In VSCode do Ctrl+Shift+p and select "conda_ssu_sustainability" as the interpreter

```
# activate conda environment
conda activate conda_ssu_sustainability

# change directory to UI folder
cd UI

# run the program
python index.py

```
This is currently a local application. Dash will be running on http://127.0.0.1:8050/



