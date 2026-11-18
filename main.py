"""
================================================================================
                    SMART STOCK PORTFOLIO TRACKER
================================================================================
A beginner-friendly, professional console application in Python 3.
Allows users to select stocks, input quantities, calculate individual and total
portfolio values using predefined stock prices, and optionally export to CSV.
================================================================================
"""

import csv
import sys

# Predefined dictionary of available stocks and their current prices (USD)
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 420.00,
    "AMZN": 190.00
}


def display_banner():
    """Displays the application's header banner."""
    print("\n" + "=" * 65)
    print("                 SMART STOCK PORTFOLIO TRACKER")
    print("=" * 65)
    print("           Track, Calculate & Manage Your Investments")
    print("=" * 65)


def display_stocks(prices):
    """
    Displays the catalog of available stocks with their unit prices.

    Args:
        prices (dict): Dictionary mapping stock ticker to unit price.
    """
    print("\n" + "-" * 65)
    print("                     AVAILABLE STOCKS")
    print("-" * 65)
    print(f" {'TICKER':<15}{'COMPANY / ASSET':<25}{'PRICE (USD)':>15} ")
    print("-" * 65)

    company_names = {
        "AAPL": "Apple Inc.",
        "TSLA": "Tesla Inc.",
        "GOOGL": "Alphabet Inc.",
        "MSFT": "Microsoft Corp.",
        "AMZN": "Amazon.com Inc."
    }

    for ticker, price in prices.items():
        name = company_names.get(ticker, "Equity")
        print(f" {ticker:<15}{name:<25}${price:>14,.2f} ")

    print("-" * 65)
    print(" Tip: Enter 'DONE' at any prompt to complete your stock selection.")
    print("-" * 65)


def get_valid_quantity():
    """
    Prompts the user for a share quantity and validates the input.

    Returns:
        int: A validated positive integer representing the number of shares.
    """
    while True:
        qty_input = input("Enter quantity: ").strip()

        # Handle empty input
        if not qty_input:
            print("[ERROR] Quantity cannot be empty. Please enter a whole number.")
            continue

        try:
            quantity = int(qty_input)

            if quantity <= 0:
                print("[ERROR] Quantity must be a positive number greater than 0.")
                continue

            return quantity

        except ValueError:
            print("[ERROR] Invalid quantity. Please enter a valid whole number (e.g., 5, 10).")


def get_portfolio_entries(prices):
    """
    Collects stock ticker symbols and quantities from the user.
    Combines quantities if the same stock symbol is entered multiple times.

    Args:
        prices (dict): Available stock prices dictionary.

    Returns:
        dict: User's portfolio mapping ticker symbols to total quantities.
    """
    portfolio = {}

    while True:
        stock_input = input("\nEnter stock symbol (or 'DONE' to finish): ").strip().upper()

        if stock_input == "DONE":
            break

        if not stock_input:
            print("[ERROR] Stock symbol cannot be empty. Try again.")
            continue

        if stock_input not in prices:
            valid_list = ", ".join(prices.keys())
            print(f"[ERROR] '{stock_input}' is not in the list of available stocks.")
            print(f"        Please choose from: {valid_list}")
            continue

        quantity = get_valid_quantity()

        # Combine quantity into portfolio dictionary
        previous_qty = portfolio.get(stock_input, 0)
        portfolio[stock_input] = previous_qty + quantity

        if previous_qty > 0:
            print(f"[SUCCESS] Updated {stock_input}: Added {quantity} share(s). "
                  f"Total shares now: {portfolio[stock_input]}")
        else:
            print(f"[SUCCESS] Added {quantity} share(s) of {stock_input} to portfolio!")

    return portfolio


def display_portfolio_summary(portfolio, prices):
    """
    Calculates individual and total investment values and displays
    a formatted summary table in the console.

    Args:
        portfolio (dict): User's portfolio {stock: quantity}.
        prices (dict): Predefined stock prices {stock: price}.

    Returns:
        tuple: (results list, total_investment float)
    """
    total_investment = 0.0
    results = []

    print("\n" + "=" * 65)
    print("                    PORTFOLIO SUMMARY")
    print("=" * 65)
    print(f" {'STOCK':<10}{'UNIT PRICE':<16}{'QUANTITY':<14}{'TOTAL VALUE':>18} ")
    print("-" * 65)

    for stock, quantity in portfolio.items():
        price = prices[stock]
        investment = price * quantity
        total_investment += investment

        results.append([
            stock,
            price,
            quantity,
            investment
        ])

        print(
            f" {stock:<10}"
            f"${price:<15,.2f}"
            f"{quantity:<14}"
            f"${investment:>17,.2f} "
        )

    print("-" * 65)
    print(f" TOTAL PORTFOLIO VALUE: {'$' + f'{total_investment:,.2f}':>39} ")
    print("=" * 65)

    return results, total_investment


def save_portfolio_to_csv(results, total_investment, filename="stock_portfolio.csv"):
    """
    Saves the calculated portfolio details into a CSV file.

    Args:
        results (list): List of [stock, price, quantity, investment] rows.
        total_investment (float): Total portfolio value.
        filename (str): Name of destination CSV file.
    """
    while True:
        save_choice = input("\nDo you want to save your portfolio to CSV? (yes/no): ").strip().lower()

        if save_choice in ("yes", "y"):
            try:
                with open(filename, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)

                    # Header Row
                    writer.writerow([
                        "Stock Symbol",
                        "Unit Price (USD)",
                        "Quantity",
                        "Investment Value (USD)"
                    ])

                    # Data Rows
                    for row in results:
                        writer.writerow([
                            row[0],
                            f"{row[1]:.2f}",
                            row[2],
                            f"{row[3]:.2f}"
                        ])

                    # Blank separator & Total row
                    writer.writerow([])
                    writer.writerow(["Total Portfolio Value", "", "", f"{total_investment:.2f}"])

                print(f"[SUCCESS] Portfolio successfully saved to '{filename}'.")
                break

            except OSError as e:
                print(f"[ERROR] Failed to save portfolio to file: {e}")
                break

        elif save_choice in ("no", "n"):
            print("[INFO] Portfolio was not saved to file.")
            break
        else:
            print("[ERROR] Please enter 'yes' or 'no'.")


def track_portfolio():
    """Main application routine for the Stock Portfolio Tracker."""
    try:
        display_banner()
        display_stocks(STOCK_PRICES)

        portfolio = get_portfolio_entries(STOCK_PRICES)

        if not portfolio:
            print("\n[INFO] No stocks were added. Portfolio is empty.")
            print("Thank you for using Stock Portfolio Tracker!")
            return

        results, total_investment = display_portfolio_summary(portfolio, STOCK_PRICES)
        save_portfolio_to_csv(results, total_investment)

        print("\nThank you for using Smart Stock Portfolio Tracker! Happy Investing!\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n[INFO] Program interrupted by user. Exiting gracefully. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    track_portfolio()

