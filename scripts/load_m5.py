from datasetsforecast.m5 import M5

Y_df, X_df, S_df = M5.load('data')

print(Y_df.shape, X_df.shape, S_df.shape)
print(Y_df.head())

# sauvegarde en parquet pour recharger vite ensuite
Y_df.to_parquet('../data/m5_sales.parquet')
X_df.to_parquet('../data/m5_exog.parquet')
S_df.to_parquet('../data/m5_static.parquet')