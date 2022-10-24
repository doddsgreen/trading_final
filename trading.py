import xlrd
import pandas as pd
from datetime import datetime, timedelta

# Create dfs
daily_email_pd = pd.DataFrame(columns=['Investor Code','Investor Name','Cell',"CCY",'Obligor','Product Code', "Maturity Date","Yield"])

# Daily emails cut off
defined_cut_off = input("Enter cut off date (yyyy-mm-dd): ")
defined_cut_off_format = datetime.strptime(defined_cut_off, '%Y-%m-%d')
defined_cut_off_format_date = defined_cut_off_format.date()

# Load redemption file
redemption_file = input("Enter path to holdings file: ")
redemption_file_read = pd.DataFrame(pd.read_excel(redemption_file))

# Trading df
trading_df = pd.DataFrame(columns=['Product Code',"CCY",'Extending','Withdrawing'])
trading_cut_off = "2022-10-24"
trading_cut_off_format = datetime.strptime(trading_cut_off, '%Y-%m-%d')
trading_cut_off_format_date = trading_cut_off_format.date()

# Trading parse
holdings_row = 0
trading_row = 0
while holdings_row < len(redemption_file_read):
    trade_date = redemption_file_read.iloc[holdings_row,9]
    trade_date_char = trade_date.date()
    next_action = redemption_file_read.iloc[holdings_row, 20]
    if trade_date_char == trading_cut_off_format_date:
        product_code = redemption_file_read.iloc[holdings_row, 7]
        # Product code in df
        if trading_df['Product Code'].eq(product_code).any() == False:
            if redemption_file_read.iloc[holdings_row, 20] == "Hold":
                ccy = redemption_file_read.iloc[holdings_row, 11]
                current_value = redemption_file_read.iloc[holdings_row, 12]
                trading_df.loc[trading_row] = [product_code, ccy, int(0), current_value]
                trading_row = trading_row+1
            if redemption_file_read.iloc[holdings_row, 20] == "Switch":
                ccy = redemption_file_read.iloc[holdings_row, 11]
                current_value = redemption_file_read.iloc[holdings_row, 12]
                trading_df.loc[trading_row] = [product_code, ccy, int(0), current_value]
                trading_row = trading_row+1
            if redemption_file_read.iloc[holdings_row, 20] == "Withdraw":
                ccy = redemption_file_read.iloc[holdings_row, 11]
                current_value = redemption_file_read.iloc[holdings_row, 12]
                trading_df.loc[trading_row] = [product_code, ccy, int(0), current_value]
                trading_row = trading_row+1       
            if redemption_file_read.iloc[holdings_row, 20] == "Auto-extend":
                ccy = redemption_file_read.iloc[holdings_row, 11]
                current_value = redemption_file_read.iloc[holdings_row, 12]
                trading_df.loc[trading_row] = [product_code, ccy, current_value, int(0)]
                trading_row = trading_row+1
            if redemption_file_read.iloc[holdings_row, 20] == "Auto-roll":
                ccy = redemption_file_read.iloc[holdings_row, 11]
                current_value = redemption_file_read.iloc[holdings_row, 12]
                trading_df.loc[trading_row] = [product_code, ccy, current_value, int(0)]
                trading_row = trading_row+1
        elif trading_df['Product Code'].eq(product_code).any() == True:
            if redemption_file_read.iloc[holdings_row, 20] == "Auto-extend":
                fill_row = trading_df.index[trading_df['Product Code']==product_code].tolist()
                extend_open = trading_df.iloc[fill_row, 2]
                extend_add = redemption_file_read.iloc[holdings_row, 12]
                extend_new = extend_open + extend_add
                trading_df.loc[trading_df["Product Code"] == product_code, 'Extending'] = extend_new
            if redemption_file_read.iloc[holdings_row, 20] == "Auto-roll":
                fill_row = trading_df.index[trading_df['Product Code']==product_code].tolist()
                extend_open = trading_df.iloc[fill_row, 2]
                extend_add = redemption_file_read.iloc[holdings_row, 12]
                extend_new = extend_open + extend_add
                trading_df.loc[trading_df["Product Code"] == product_code, 'Extending'] = extend_new
            if redemption_file_read.iloc[holdings_row, 20] == "Withrdaw":
                fill_row = trading_df.index[trading_df['Product Code']==product_code].tolist()
                withdraw_open = trading_df.iloc[fill_row, 3]
                withdraw_add = redemption_file_read.iloc[holdings_row, 12]
                withdraw_new = withdraw_open + withdraw_add
                trading_df.loc[trading_df["Product Code"] == product_code, 'Withdrawing'] = withdraw_new
            if redemption_file_read.iloc[holdings_row, 20] == "Hold":
                fill_row = trading_df.index[trading_df['Product Code']==product_code].tolist()
                withdraw_open = trading_df.iloc[fill_row, 3]
                withdraw_add = redemption_file_read.iloc[holdings_row, 12]
                withdraw_new = withdraw_open + withdraw_add
                trading_df.loc[trading_df["Product Code"] == product_code, 'Withdrawing'] = withdraw_new
            if redemption_file_read.iloc[holdings_row, 20] == "Switch":
                fill_row = trading_df.index[trading_df['Product Code']==product_code].tolist()
                withdraw_open = trading_df.iloc[fill_row, 3]
                withdraw_add = redemption_file_read.iloc[holdings_row, 12]
                withdraw_new = withdraw_open + withdraw_add
                trading_df.loc[trading_df["Product Code"] == product_code, 'Withdrawing'] = withdraw_new
        else:
            pass
    else:
        pass
    holdings_row = holdings_row + 1

# Print
with pd.ExcelWriter("Trading_Final.xlsx") as writer:
    trading_df.to_excel(writer, sheet_name = "Trading Breakdown")
