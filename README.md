# Adaptive-Solar-EV-Charging

This script allows you to charge your electric vehicle with solar power in an intelligent way that maximizes your use of clean energy. It retrieves solar and home energy data from an API and then calculates the available and maximum charging power for an electric vehicle. It then uses this information to either allow or prevent charging of the vehicle and sets the appropriate charging current.

 ## Prerequisites
  To use this script, you will need:

   - Python 3.7 or higher installed on your computer
   - Git installed on your computer
   - An API that provides solar and home energy data
 ## Installation
  - Clone the repository using the following command:
  
  ```
   git clone https://github.com/Duncan1106/ev-charging-script.git
  ```
  
  - Edit the config.py file to include the URL of your API. (not implemented yet)

 ## Run the script using the following command:
  ``` 
  python main.py --buffer <buffer_power> --style <charging_style> 
  ```
  
 ## Usage
   To use the script, simply run it using the command specified above. 
   - The --buffer argument specifies the amount of power that should remain untouched and not be used for EV charging. This power should be available for other home consumers. 
   - The --style argument specifies the style in which the EV should get charged:
   
     - A more aggressive charging style should result in fewer stops but potentially more power drawn from the grid.
     - A more conservative charging style should result in more stops but nearly no power drawn from the grid.

 ## Contributing
  Contributions to this project are welcome. To contribute, follow these steps:
  
   - Fork this repository
   - Create a new branch
   - Make your changes
   - Test your changes
   - Submit a pull request

 ## License
  This project is licensed under the MIT License - see the LICENSE file for details.
