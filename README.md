# README

This repository hosts code that can be used to reproduce the analysis used in the Lumos Health article, [*How will my medical costs increase with age?*](www.google.com).

To run the analysis simply open up main.ipynb with jupyter lab and run the cells.  You can run the following code to open the file.

Overview of other files:
- **pop_ffm_states.csv**  :  reference data on population of ffm states used to narrow down which states are used when arriving at the median health insurance premium for marketplace plans.
- **prepare_base_data.py**  :  processes MEPS data to limit our population only to folks with private and insurance and no other payment sources outside of the insurance and themselves.  Run from main.ipynb and utilizes base_data_lookup.csv
