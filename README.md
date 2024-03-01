# Route Optimization with Clark and Wright Method

This script aims to optimize routes for delivery trucks using the Clark and Wright method. It reads data from Excel sheets containing hierarchy information and location details, then generates optimal routes considering capacity, time, and speed constraints.

## Requirements

- Python 3.x
- Pandas library

## Inputs

- **Hierarchical Data**: Excel sheet containing hierarchy information (`Trabalho 1 - Deadline 24_05 (2) (1).xlsx`, sheet name: "Página7").
- **Location Information**: Excel sheet containing location details (`Trabalho 1 - Deadline 24_05 (2) (1).xlsx`, sheet name: "Página8").

## Outputs

- **Optimized Routes**: The script outputs optimized routes in dictionary format. Each route is represented as a list of locations.

## Configuration

- **Capacity Constraint (`CAP`)**: Maximum load capacity of delivery trucks (default: 2800 kg).
- **Time Constraint (`TEMPO`)**: Maximum time limit for delivery routes in minutes (default: 8 hours).
- **Speed (`KM_H`)**: Average speed of delivery trucks in kilometers per hour (default: 60 km/h).

## Additional Notes

- The script may take some time to execute depending on the size of the input data.
- Optimization results may vary based on input data and constraints.
