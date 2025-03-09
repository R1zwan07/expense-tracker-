import streamlit as st  # For creating the web interface
import pandas as pd  # For handling and manipulating data
import os  # For file operations

# Function to load existing expenses from a CSV file
def load_expenses():
    """
    Loads the expenses from 'expenses.csv' if it exists.
    Converts 'Amount' to numeric and 'Date' to datetime for proper handling.
    
    Returns:
        pd.DataFrame: A DataFrame containing the expenses data.
    """
    if os.path.exists("expenses.csv"):
        expenses = pd.read_csv("expenses.csv")
        expenses["Amount"] = pd.to_numeric(expenses["Amount"], errors="coerce")  # Ensure numeric data in 'Amount'
        expenses["Date"] = pd.to_datetime(expenses["Date"], errors="coerce")  # Ensure datetime data in 'Date'
        return expenses
    else:
        return pd.DataFrame(columns=["Description", "Amount", "Date"])

# Function to save a new expense
def save_expense(description, amount, date):
    """
    Saves a new expense to the 'expenses.csv' file.
    
    Args:
        description (str): Description of the expense.
        amount (float): Amount of the expense.
        date (str): Date of the expense.
    """
    new_data = pd.DataFrame([[description, amount, date]], columns=["Description", "Amount", "Date"])
    if os.path.exists("expenses.csv"):
        new_data.to_csv("expenses.csv", mode='a', header=False, index=False)
    else:
        new_data.to_csv("expenses.csv", mode='w', index=False)

# Function to remove an expense
def remove_expense(index):
    """
    Removes an expense by its index from the 'expenses.csv' file.
    
    Args:
        index (int): Index of the expense to remove.
    """
    expenses = load_expenses()
    expenses = expenses.drop(index)
    expenses.to_csv("expenses.csv", index=False)

# Function to filter expenses
def filter_expenses(expenses, description_filter, amount_filter, date_range):
    """
    Filters the expenses based on description, amount, and date range.
    
    Args:
        expenses (pd.DataFrame): The expenses DataFrame to filter.
        description_filter (str): Keyword to filter by description.
        amount_filter (float): Maximum amount to filter by.
        date_range (list): List with two dates [start_date, end_date] to filter by.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    filtered_expenses = expenses.copy()
    
    # Apply description filter
    if description_filter:
        filtered_expenses = filtered_expenses[filtered_expenses['Description'].str.contains(description_filter, case=False, na=False)]
    
    # Apply amount filter
    if amount_filter > 0:
        filtered_expenses = filtered_expenses[filtered_expenses['Amount'] <= amount_filter]
    
    # Apply date range filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_expenses = filtered_expenses[
            (filtered_expenses['Date'] >= pd.to_datetime(start_date)) &
            (filtered_expenses['Date'] <= pd.to_datetime(end_date))
        ]

    return filtered_expenses

# Main Streamlit App
def main():
    """
    Main function to render the Streamlit application for tracking expenses.
    """
    st.title("Expense Tracker")

    # Load the current expenses
    expenses = load_expenses()

    # Display current expenses
    st.header("Current Expenses")
    if not expenses.empty:
        st.dataframe(expenses)  # Show the expenses in a table format
        selected_expense = st.selectbox("Select an expense to remove", expenses.index)
        if st.button("Remove Expense"):
            remove_expense(selected_expense)
            st.success("Expense removed successfully!")
            expenses = load_expenses()  # Reload updated expenses
            st.dataframe(expenses)
    else:
        st.write("No expenses found.")

    # Section to add new expenses
    st.subheader("Add New Expense")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")

    if st.button("Add Expense"):
        if description and amount > 0:
            save_expense(description, amount, date)
            st.success(f"Added: {description} - {amount} on {date}")
            expenses = load_expenses()  # Reload updated expenses
            st.dataframe(expenses)
        else:
            st.error("Please enter a valid description and amount.")

    # Section to filter expenses
    st.subheader("Filter Expenses")
    description_filter = st.text_input("Filter by Description")
    amount_filter = st.number_input("Filter by Maximum Amount", min_value=0.0, format="%.2f")
    date_range = st.date_input("Filter by Date Range", [])

    if st.button("Apply Filter"):
        filtered_expenses = filter_expenses(expenses, description_filter, amount_filter, date_range)
        st.write(f"Filtered Expenses:")
        st.dataframe(filtered_expenses)

# Run the app
if __name__ == "__main__":
    main()
