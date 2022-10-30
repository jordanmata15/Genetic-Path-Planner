# Genetic-Path-Planner

Genetic algorithm solution for minimizing the distance traveled by N trucks (default 2) to P different homes (default 45).

# Running
Running the algorithm will automatically create a log file in `./data`

1. Navigate to `./src` directory via terminal
2. (Optional) Update values of `crossover_probability`, `num_chromosomes`, etc at the very bottom in main()
3. Run `python3 Genetic_Path_Planner.py` (assumes you have python3 in your PATH. Otherwise use the full python3 binary path)
4. (Optional) Rerun ALL of the the plots for each csv file: 
              Navigate to `./scripting` directory
              Run `python3 plot.py`
6. Navigate to `./data`
7. View plots as png files

# Data and Plotting
Running `Genetic_Path_Planner.py` will generate a csv file according to the percentage of crossover. If 10% crossover is passed in, then it will produce a file in the `data` directory called `data_10_pct.csv`.

Once the *.csv file is generated, if we run `scripting/plot.py` this will rerun the plots for ALL csv files in the `data` directory and will output them as x_pct.png. For example, if we have `data_10_pct.csv` and `data_20_pct.csv` in the `data` directory, then BOTH `10_pct.png` and `20_pct.png` will be generated. The script will loop over all csv files and regenerate the plot.

If you wish to generate new plots, it's recommended to empty out the `data` directory first.
