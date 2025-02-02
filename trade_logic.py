# trade_logic.py

import pyperclip
from tkinter import messagebox

# Global data
saved_trades = []
starting_balance = 0.0

def set_starting_balance(new_balance_entry, summary_update_callback):

    global starting_balance
    try:
        new_balance = float(new_balance_entry.get())
        starting_balance = new_balance
        summary_update_callback()
        messagebox.showinfo("Balance Set", f"Starting balance set to {starting_balance:.6f} SOL.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric value for the starting balance.")

def save_trade(
    invested_sol_entry, 
    gain_percents_entry, 
    sold_percentages_entry, 
    priority_fee_entry, 
    bribe_fee_entry,
    update_callback
):

    global starting_balance, saved_trades
    try:
        invested_sol = float(invested_sol_entry.get())
        gain_percents = gain_percents_entry.get().split(',')
        sold_percentages = sold_percentages_entry.get().split(',')
        priority_fee = float(priority_fee_entry.get())
        bribe_fee = float(bribe_fee_entry.get())

        # Clean up strings and convert to float
        gain_percents = [float(x.strip()) for x in gain_percents if x.strip()]
        sold_percentages = [float(x.strip()) for x in sold_percentages if x.strip()]

        if len(gain_percents) != len(sold_percentages):
            messagebox.showerror("Input Error", 
                "The number of gain percentages and sold percentages must be the same.")
            return

        remaining_amount = invested_sol

        for gain_percent, sold_percent in zip(gain_percents, sold_percentages):
            # Calculate the amount sold as a percentage of the remaining amount
            sold_amount = remaining_amount * (sold_percent / 100)
            # BullX fee (1% on sold portion)
            bullx_fee = sold_amount * 0.01
            # Solana Fees
            solana_base_fee = 0.000005
            solana_total_fee = solana_base_fee + priority_fee + bribe_fee
            # Total fees
            total_fees = bullx_fee + solana_total_fee
            # Net investment after fees
            net_investment = sold_amount - total_fees
            # Gains
            gross_gain = net_investment * (gain_percent / 100)
            net_gain = gross_gain - total_fees
            # Update balance
            starting_balance += net_gain

            # Save trade details
            trade = {
                "Invested SOL": invested_sol,
                "Sold Percent": sold_percent,
                "Sold Amount": sold_amount,
                "Remaining Amount": remaining_amount - sold_amount,
                "Gain %": gain_percent,
                "Net Gain": net_gain,
                "Priority Fee": priority_fee,
                "Bribe Fee": bribe_fee
            }
            saved_trades.insert(0, trade)  # newest trade at the top

            remaining_amount -= sold_amount

        # Refresh GUI
        update_callback()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def delete_trade(index, update_callback):
    """
    Deletes a trade at the given index from saved_trades,
    adjusts global starting_balance, and triggers a GUI update.
    """
    global starting_balance, saved_trades
    if 0 <= index < len(saved_trades):
        starting_balance -= saved_trades[index]['Net Gain']
        del saved_trades[index]
        update_callback()

def copy_trades():
    """
    Copies all trade details in a structured text format to the clipboard.
    """
    trades_text = "\n".join([
        (
            f"Invested SOL: {trade['Invested SOL']:.4f}, "
            f"Sold Percent: {trade['Sold Percent']:.2f}%, "
            f"Sold Amount: {trade['Sold Amount']:.4f}, "
            f"Remaining Amount: {trade['Remaining Amount']:.4f}, "
            f"Gain %: {trade['Gain %']:.2f}%, "
            f"Net Gain: {trade['Net Gain']:.6f}"
        ) for trade in saved_trades
    ])
    pyperclip.copy(trades_text)
    messagebox.showinfo("Copied", "Trades have been copied to clipboard.")

def copy_final_amount(summary_label):
    """
    Copies the final amounts text from summary_label to the clipboard.
    """
    final_text = summary_label.cget("text")
    pyperclip.copy(final_text)
    messagebox.showinfo("Copied", "Final amounts have been copied to clipboard.")

def get_saved_trades():
    """
    Returns the current list of saved trades.
    """
    global saved_trades
    return saved_trades

def get_starting_balance():
    """
    Returns the current global starting_balance.
    """
    global starting_balance
    return starting_balance
