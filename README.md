🚚 Transportation Problem Solver

Welcome to the Transportation Problem Solver! This application allows you to solve transportation problems using various methods from Operations Research. It provides a graphical user interface (GUI) to input your data and see step-by-step solutions for better understanding.

📖 Overview

This solver includes the following methods:

Northwest Corner Method (NWC)
Vogel's Approximation Method (VAM)
Least Cost Method (LCM)
Stepping Stone Method
MODI Method (Modified Distribution Method)
🛠 Features

User-Friendly Interface: Built with Tkinter for easy interaction.
Step-by-Step Solutions: Navigate through each iteration to understand the process.
Visualization: See all cell values and how they change in each step.
Final Cost Display: Get the total cost (Z) at the end of the computation.
📋 Requirements

Python 3.x installed on your system.
Tkinter library (usually included with Python).
💻 Installation and Running Steps

Follow these steps to run the application:

1️⃣ Clone the Repository
Clone the repository to your local machine using Git:

git clone https://github.com/yourusername/transportation-problem-solver.git
2️⃣ Navigate to the Project Directory
Change your current directory to the project's root directory:

cd transportation-problem-solver
3️⃣ Run the Application
Execute the main script to start the application:

python main.py
If python points to Python 2.x, use:

python3 main.py
📝 How to Use the Application

Select the Method:
Choose the desired method from the dropdown menu on the main window.
Enter the Number of Suppliers and Consumers:
Input the number of suppliers and consumers in the provided fields.
Click on "Enter Data" to proceed.
Input the Data:
A new window will appear where you can input the cost matrix, supply, and demand values.
Fill in all the required fields with numerical values.
Solve the Problem:
Click on the "Solve" button to compute the solution.
If the problem is unbalanced (total supply ≠ total demand), the application will prompt an error.
View the Solution:
Navigate through each step using the "Previous" and "Next" buttons.
All cell values, including costs and allocations, are displayed.
Upon reaching the final step, a message box will display the total cost (Z) of the solution.
⚠️ Important Notes

Balanced Problem Required: The application requires the transportation problem to be balanced. Ensure that the total supply equals the total demand before solving.
Complete Implementations: All methods are fully implemented without any simplifications.
Dependencies: No external libraries are needed beyond Tkinter and Python's standard libraries.
🐞 Troubleshooting

Tkinter Module Not Found:
Ensure that Tkinter is installed. It usually comes with Python, but if not, you may need to install it separately depending on your operating system.
Python Version Issues:
The application is designed for Python 3.x. Running it with Python 2.x will result in errors.
🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request with a detailed description of your changes.
📄 License

This project is licensed under the MIT License. See the LICENSE file for details.