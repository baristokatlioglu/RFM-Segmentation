import datetime as dt
import pandas as pd

# pd.set_option('display.max_columns', None)     setting for displaying columns
# pd.set_option('display.max_rows', None)        setting for displaying rows
# pd.set_option('display.float_format', lambda x: '%.5f' % x)   adjusting the display of decimal expressions


# Reading data
df_ = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

# Dataset overview
df.shape
df.dtypes
df.describe().T

# Missing value check
df.isnull().sum()

# Deleting missing values
df.dropna(inplace=True)
df.isnull().sum()

# Number of unique classes in StockCode
df["StockCode"].nunique()

# Multiplexing control in StockCode
df["StockCode"].value_counts()

# Preparation of the data set
df.groupby("StockCode").agg({"Quantity": "sum"}).sort_values(by="Quantity", ascending=False).head(5)

df = df[~df["Invoice"].str.contains("C", na=False)]
df.head()

df = df[df["Price"] > 0]
df = df[df["Quantity"] > 0]
df["TotalPrice"] = df["Price"] * df["Quantity"]



# Recency, time since customer's last purchase
# Frequency is the total purchase made by the customer.
# Monetary, the total money earned by the customer
today_date = dt.datetime(2011,12,11)

rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda InvoiceDate: (today_date-InvoiceDate.max()).days,
                               "Invoice" : lambda Invoice : Invoice.nunique(),
                               "TotalPrice" : lambda TotalPrice : TotalPrice.sum()})
rfm.head()
rfm.columns = ["recency", "frequency", "monetary"]
rfm.head()
rfm = rfm[rfm["monetary"] > 0]

# Generating RFM scores
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])
rfm.head()

rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str)+rfm["frequency_score"].astype(str))

# Classification of customers based on RFM scores
seg_map = {
    r'[1-2][1-2]' : 'hibernating',
    r'[1-2][3-4]' : 'at_Risk',
    r'[1-2]5' : 'cant_loose',
    r'3[1-2]' : 'about_to_sleep',
    r'33' : 'need_attention',
    r'[3-4][4-5]' : 'loyal_customers',
    r'41' : 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]' : 'potential_loyalists',
    r'5[4-5]' : 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

# GÖREV 5

# new customers,
# offers can be created that will convert them from one-time customers to more. like up-sell , cross-sell

# potential_loyalists,
# a membership program with certain benefits, by creating customer incentives for them, sending gifts
# by creating etc. actions can be made.

# cant_loose,
# they can be contacted according to their personal preferences.


# Writing index information of Loyal Customers to excel
loyals=rfm[rfm["segment"] == 'loyal_customers'].index
loyals = pd.DataFrame(loyals)
loyals.to_excel("loyal_customers_id.xlsx")






