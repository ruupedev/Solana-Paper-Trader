# Crypto Day Trading Calculator

**Crypto Day Trading Calculator** is a Python-based tool that simplifies day trading calculations for cryptocurrencies. It helps traders track their trades, manage starting balances, calculate gains, and record transaction fees. The project includes a graphical user interface (GUI) for intuitive use, making it accessible for all skill levels.

🚀 Features  
📊 Track Trades: Save and manage individual trade details, including invested amounts, sold percentages, and net gains.  
💰 Fee Calculations: Automatically calculate priority and bribe fees for Solana-based transactions.  
📋 Clipboard Integration: Copy trade summaries and final account details directly to the clipboard.  
📈 Win/Loss Analysis: View insights like win/loss ratio, average win, and average loss.  
💾 Exportable Data: Allows easy copying of all trade data for record-keeping.  
⚙️ Customizable Inputs: Adjust gain percentages, sold percentages, and fees for dynamic scenarios.

📁 Files  
main.py: Entry point of the application. It initializes and launches the GUI.  
trade_logic.py: Handles all trade-related calculations, such as fee processing and balance updates.  
ui.py: Builds the user interface, including input fields, tables, and buttons for user interaction.  
Launch.bat: Batch file for quick launching of the program on Windows.

📌 How It Works  
Set Starting Balance:  
- Input your initial balance in SOL (e.g., `1.0000 SOL`).  
- Click "Set Balance" to save it.  
Add Trades:  
- Input invested amount, gain percentages, and sold percentages.  
- Specify transaction fees (priority and bribe fees).  
- Click "Save Trades" to calculate and save the trade details.  
Analyze Data:  
- View a detailed summary of gains/losses in the right-hand panel.  
- Analyze trades in the interactive table, including individual fees and remaining balances.  
Export Data:  
- Use the "Copy Trades" or "Copy Final" buttons to export data to the clipboard for further use.

🔧 Requirements  
- Python 3.10 or newer  
- Dependencies:  
  - `tkinter`: For GUI  
  - `pyperclip`: For clipboard functionality  

Install dependencies with:  
```bash
pip install pyperclip
```

🚀 Installation and Launch  
Clone the Repository:  
```bash
git clone https://github.com/ruupedev/Crypto-Day-Trading-Calculator.git
cd Crypto-Day-Trading-Calculator
```  
Run the Program:  
Option 1 (Python):  
```bash
python main.py
```  
Option 2 (Windows Batch File): Double-click the `Launch.bat` file to start the program.

🤝 Contributions  
Feel free to contribute by:  
- Reporting bugs  
- Suggesting new features  
- Submitting pull requests

📜 License  
This project is licensed under the MIT License. See the LICENSE file for more details.

📞 Contact  
For questions or feedback, contact Ruupe Sirviö at [ruupesirvio@gmail.com](mailto:ruupesirvio@gmail.com).

Let me know if you'd like additional sections or modifications! 🚀
