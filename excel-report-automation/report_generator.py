import pandas as pd

INPUT_FILE = "sample_input.xlsx"
OUTPUT_FILE = "cleaned_report.xlsx"

def load_data(file):
    df = pd.read_excel(file)
    # Remove duplicates
    df = df.drop_duplicates()
    # Fill missing values
    df['Quantity'] = df['Quantity'].fillna(0)
    df['Price'] = df['Price'].fillna(0)
    return df

def generate_summary(df):
    summary = {}
    summary['Total Sales'] = (df['Quantity'] * df['Price']).sum()
    summary['Total Products Sold'] = df['Quantity'].sum()
    summary['Number of Orders'] = len(df)
    return summary

def top_products(df, n=5):
    df['Total'] = df['Quantity'] * df['Price']
    top = df.groupby('Product')['Total'].sum().sort_values(ascending=False).head(n)
    return top

def monthly_revenue(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby('Month')['Total'].sum()
    return monthly

def main():
    df = load_data(INPUT_FILE)
    summary = generate_summary(df)
    top = top_products(df)
    monthly = monthly_revenue(df)

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)
        top.to_frame(name="Total Revenue").to_excel(writer, sheet_name="Top Products")
        monthly.to_frame(name="Revenue").to_excel(writer, sheet_name="Monthly Revenue")

    print(f"Report generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()