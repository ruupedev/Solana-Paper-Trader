# ui.py

import tkinter as tk
from tkinter import ttk, Scrollbar, Canvas, messagebox
import pyperclip

# ----------------------------------------------------------------
#  GLOBALS (Demo only; normally you'd separate logic from UI)
# ----------------------------------------------------------------
saved_trades = []
starting_balance = 0.0

# ----------------------------------------------------------------
#  LOGIC
# ----------------------------------------------------------------
def set_starting_balance(entry, update_ui):
    global starting_balance
    try:
        bal = float(entry.get())
        starting_balance = bal
        update_ui()
        messagebox.showinfo("Balance Set", f"Starting balance set to {bal:.6f} SOL.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric value.")

def save_trade(e_invested, e_gain, e_sold, e_priority, e_bribe, update_ui):
    global starting_balance, saved_trades
    try:
        invested = float(e_invested.get())
        gain_percents = e_gain.get().split(',')
        sold_percents = e_sold.get().split(',')
        priority_fee = float(e_priority.get())
        bribe_fee = float(e_bribe.get())

        gain_percents = [float(x.strip()) for x in gain_percents if x.strip()]
        sold_percents = [float(x.strip()) for x in sold_percents if x.strip()]

        if len(gain_percents) != len(sold_percents):
            messagebox.showerror("Input Error", 
                "The number of gain percentages and sold percentages must match.")
            return

        remaining = invested
        for gp, sp in zip(gain_percents, sold_percents):
            sold_amt = remaining * (sp / 100)
            bullx_fee = sold_amt * 0.01
            sol_fee = 0.000005 + priority_fee + bribe_fee
            total_fees = bullx_fee + sol_fee
            net_invest = sold_amt - total_fees
            gross_gain = net_invest * (gp / 100)
            net_gain = gross_gain - total_fees

            starting_balance += net_gain

            trade = {
                "Invested SOL": invested,
                "Sold %": sp,
                "Sold Amount": sold_amt,
                "Remaining": remaining - sold_amt,
                "Gain %": gp,
                "Net Gain": net_gain
            }
            saved_trades.insert(0, trade)
            remaining -= sold_amt

        update_ui()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def delete_trade(index, update_ui):
    global starting_balance, saved_trades
    if 0 <= index < len(saved_trades):
        starting_balance -= saved_trades[index]["Net Gain"]
        del saved_trades[index]
        update_ui()

def copy_trades():
    trades_text = "\n".join([
        (
            f"Invested SOL: {t['Invested SOL']:.4f}, "
            f"Sold %: {t['Sold %']:.2f}%, "
            f"Sold Amount: {t['Sold Amount']:.4f}, "
            f"Remaining: {t['Remaining']:.4f}, "
            f"Gain %: {t['Gain %']:.2f}%, "
            f"Net Gain: {t['Net Gain']:.6f}"
        )
        for t in saved_trades
    ])
    pyperclip.copy(trades_text)
    messagebox.showinfo("Copied", "Trades copied to clipboard.")

def copy_final_amount(summary_label):
    text = summary_label.cget("text")
    pyperclip.copy(text)
    messagebox.showinfo("Copied", "Final amounts copied to clipboard.")

# ----------------------------------------------------------------
#  MAIN UI
# ----------------------------------------------------------------
def run_app():
    root = tk.Tk()
    root.title("Crypto Day Trading Calculator")
    root.geometry("700x600")  # Start size: 900x700
    root.configure(bg="#1A1A1A")

    # =======================
    # STYLE SETUP
    # =======================
    style = ttk.Style()
    style.theme_use("clam")  # Good base for custom

    # 1) "RoundedFrame.TFrame" with no visible border lines
    style.configure(
        "RoundedFrame.TFrame",
        background="#2B2B2B",
        borderwidth=0,
        relief="flat",
        # Padding can simulate extra space;  "rounded" corners need custom images
    )

    # 2) Label style
    style.configure(
        "DarkLabel.TLabel",
        background="#2B2B2B",
        foreground="#FFFFFF",
        font=("Segoe UI", 10)
    )

    # 3) Purple button style: no lines
    style.configure(
        "PurpleButton.TButton",
        background="#9B59B6",
        foreground="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=6
    )
    style.map(
        "PurpleButton.TButton",
        background=[("active", "#BB8FCE")]  # lighter purple on hover
    )

    # =======================
    # TITLE
    # =======================
    title_label = tk.Label(
        root,
        text="Crypto Day Trading Calculator",
        bg="#1A1A1A",
        fg="#BB8FCE",
        font=("Segoe UI", 20, "bold")
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # =======================
    # LEFT FRAME - Inputs
    # =======================
    left_frame = ttk.Frame(root, style="RoundedFrame.TFrame")
    left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")

    # Callback to refresh the trades table
    def update_after_balance():
        rebuild_trades()

    # Row 0: Starting SOL
    lbl_start_bal = ttk.Label(left_frame, text="Starting SOL Balance:", style="DarkLabel.TLabel")
    lbl_start_bal.grid(row=0, column=0, padx=8, pady=8, sticky="w")

    entry_start_bal = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_start_bal.grid(row=0, column=1, padx=5, pady=8)

    btn_balance = ttk.Button(
        left_frame,
        text="Set Balance",
        style="PurpleButton.TButton",
        command=lambda: set_starting_balance(entry_start_bal, update_after_balance)
    )
    btn_balance.grid(row=0, column=2, padx=10, pady=8)

    # Row 1: Invested SOL
    lbl_invested = ttk.Label(left_frame, text="Invested SOL:", style="DarkLabel.TLabel")
    lbl_invested.grid(row=1, column=0, padx=8, pady=8, sticky="w")

    entry_invested = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_invested.grid(row=1, column=1, padx=5, pady=8)

    # Row 2: Gain Percentages
    lbl_gain = ttk.Label(left_frame, text="Gain Percentages:", style="DarkLabel.TLabel")
    lbl_gain.grid(row=2, column=0, padx=8, pady=8, sticky="w")

    entry_gain = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_gain.grid(row=2, column=1, padx=5, pady=8)

    # Row 3: Sold Percentages
    lbl_sold = ttk.Label(left_frame, text="Sold Percentages:", style="DarkLabel.TLabel")
    lbl_sold.grid(row=3, column=0, padx=8, pady=8, sticky="w")

    entry_sold = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_sold.grid(row=3, column=1, padx=5, pady=8)

    # Row 4: Priority Fee
    lbl_pri = ttk.Label(left_frame, text="Priority Fee (SOL):", style="DarkLabel.TLabel")
    lbl_pri.grid(row=4, column=0, padx=8, pady=8, sticky="w")

    entry_priority = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_priority.insert(0, "0.0001")
    entry_priority.grid(row=4, column=1, padx=5, pady=8)

    # Row 5: Bribe Fee
    lbl_bribe = ttk.Label(left_frame, text="Bribe Fee (SOL):", style="DarkLabel.TLabel")
    lbl_bribe.grid(row=5, column=0, padx=8, pady=8, sticky="w")

    entry_bribe = ttk.Entry(left_frame, width=18, font=("Segoe UI", 10))
    entry_bribe.insert(0, "0.0001")
    entry_bribe.grid(row=5, column=1, padx=5, pady=8)

    # Buttons (row 6)
    def save_trade_and_update():
        save_trade(entry_invested, entry_gain, entry_sold, entry_priority, entry_bribe, rebuild_trades)

    btn_frame = ttk.Frame(left_frame, style="RoundedFrame.TFrame")
    btn_frame.grid(row=6, column=0, columnspan=3, pady=10)

    btn_save = ttk.Button(btn_frame, text="Save Trades", style="PurpleButton.TButton",
                          command=save_trade_and_update)
    btn_save.pack(side=tk.LEFT, padx=5)

    btn_copy_t = ttk.Button(btn_frame, text="Copy Trades", style="PurpleButton.TButton",
                            command=copy_trades)
    btn_copy_t.pack(side=tk.LEFT, padx=5)

    def copy_final_cb():
        copy_final_amount(summary_label)

    btn_copy_f = ttk.Button(btn_frame, text="Copy Final", style="PurpleButton.TButton",
                            command=copy_final_cb)
    btn_copy_f.pack(side=tk.LEFT, padx=5)

    # =======================
    # RIGHT FRAME - Summary
    # =======================
    right_frame = ttk.Frame(root, style="RoundedFrame.TFrame")
    right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ne")

    summary_label = ttk.Label(right_frame, text="", style="DarkLabel.TLabel",
                              font=("Segoe UI", 10), background="#2B2B2B",
                              foreground="#FFFFFF", justify=tk.LEFT)
    summary_label.pack(padx=10, pady=10)

    # =======================
    # BOTTOM - TRADES TABLE
    # =======================
    trades_canvas = tk.Canvas(root, bg="#1A1A1A", highlightthickness=0)
    trades_canvas.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0,20))

    scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=trades_canvas.yview)
    scrollbar_y.grid(row=2, column=2, sticky="ns", pady=(0,20))

    trades_canvas.configure(yscrollcommand=scrollbar_y.set)

    trades_frame = ttk.Frame(trades_canvas, style="RoundedFrame.TFrame")
    trades_canvas.create_window((0, 0), window=trades_frame, anchor="nw")

    def on_frame_configure(event):
        trades_canvas.configure(scrollregion=trades_canvas.bbox("all"))

    trades_frame.bind("<Configure>", on_frame_configure)

    # Let the bottom row expand
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # =======================
    # REBUILD TABLE FUNCTION
    # =======================
    def rebuild_trades():
        # Clear old
        for w in trades_frame.winfo_children():
            w.destroy()

        headers = ["Invested SOL", "Sold %", "Sold Amount", "Remaining", "Gain %", "Net Gain", "Delete"]
        header_bg = "#4A4A4A"
        header_fg = "#FFFFFF"
        row_bg1 = "#2E2E2E"
        row_bg2 = "#3C3C3C"

        # Header row
        for col_i, head in enumerate(headers):
            lbl_h = tk.Label(
                trades_frame,
                text=head,
                font=("Segoe UI", 9, "bold"),
                bg=header_bg,
                fg=header_fg,
                width=12,
                pady=5
            )
            lbl_h.grid(row=0, column=col_i, sticky="nsew", padx=1, pady=1)

        # Summary
        global starting_balance
        total_sol = sum(t["Net Gain"] for t in saved_trades)
        wins = len([t for t in saved_trades if t["Net Gain"] > 0])
        losses = len(saved_trades) - wins
        if (wins + losses) == 0:
            win_loss_ratio = "N/A"
        else:
            win_loss_ratio = f"{wins}:{losses}" if losses else "All Wins"

        avg_win = sum(t["Net Gain"] for t in saved_trades if t["Net Gain"] > 0) / wins if wins else 0
        avg_loss = sum(t["Net Gain"] for t in saved_trades if t["Net Gain"] < 0) / losses if losses else 0

        summary_label.config(
            text=(
                f"Final Amounts:\n"
                f"Starting Balance: {starting_balance:.6f} SOL\n"
                f"Net Gain/Loss: {total_sol:.6f} SOL\n"
                f"Win/Loss Ratio: {win_loss_ratio}\n"
                f"Average Win: {avg_win:.6f} SOL\n"
                f"Average Loss: {avg_loss:.6f} SOL"
            )
        )

        # Rows
        for row_i, trade in enumerate(saved_trades, start=1):
            bgc = row_bg1 if row_i % 2 else row_bg2
            data_cols = [
                f"{trade['Invested SOL']:.4f}",
                f"{trade['Sold %']:.2f}%",
                f"{trade['Sold Amount']:.4f}",
                f"{trade['Remaining']:.4f}",
                f"{trade['Gain %']:.2f}%",
                f"{trade['Net Gain']:.6f}"
            ]
            for col_j, val in enumerate(data_cols):
                lbl_d = tk.Label(
                    trades_frame,
                    text=val,
                    font=("Segoe UI", 9),
                    bg=bgc,
                    fg="#FFFFFF",
                    width=12,
                    anchor="center"
                )
                lbl_d.grid(row=row_i, column=col_j, sticky="nsew", padx=1, pady=1)

            # Delete button (X)
            btn_del = tk.Button(
                trades_frame,
                text="X",
                command=lambda idx=row_i-1: delete_trade(idx, rebuild_trades),
                bg="#E74C3C",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                width=3
            )
            btn_del.grid(row=row_i, column=len(data_cols), sticky="nsew", padx=1, pady=1)

        for c in range(len(headers)):
            trades_frame.grid_columnconfigure(c, weight=1)

    # INIT
    rebuild_trades()
    root.mainloop()

if __name__ == "__main__":
    run_app()
