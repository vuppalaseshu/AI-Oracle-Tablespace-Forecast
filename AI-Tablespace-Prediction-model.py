import pandas as pd
from prophet import Prophet

# ------------------------------------
# Load Data
# ------------------------------------

history = pd.read_csv("C:\\Users\\Pavan.Vuppala\\OneDrive - Entain Group\\Desktop\\Pavan\\DataScience\\Oracle-DB-Project\\Git-Hub\\tablespace_history_20260306.csv")
thresholds = pd.read_csv("C:\\Users\\Pavan.Vuppala\\OneDrive - Entain Group\\Desktop\\Pavan\\DataScience\\Oracle-DB-Project\\Git-Hub\\tablespace_thresholds_20260306.csv")

history['ROLLUP_TIMESTAMP'] = pd.to_datetime(history['ROLLUP_TIMESTAMP'], format='%d-%b-%y')

results = []

# ------------------------------------
# Loop through each DB and tablespace
# ------------------------------------

for (db, ts), group in history.groupby(['TARGET_NAME','TABLESPACE']):

    df = group[['ROLLUP_TIMESTAMP','USED_PCT']].copy()

    if len(df) < 10:
        continue

    df = df.rename(columns={
        'ROLLUP_TIMESTAMP':'ds',
        'USED_PCT':'y'
    })

    # Get thresholds
    t = thresholds[
        (thresholds['TARGET_NAME']==db) &
        (thresholds['KEY_VALUE']==ts)
    ]

    if t.empty:
        continue

    warning = t['WARNING_THRESHOLD'].values[0]
    critical = t['CRITICAL_THRESHOLD'].values[0]

    # Train Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Predict next 180 days
    future = model.make_future_dataframe(periods=120)
    forecast = model.predict(future)

    forecast = forecast[['ds','yhat']]

    # ------------------------------------
    # Detect threshold crossing
    # ------------------------------------

    warning_date = None
    critical_date = None

    for _, row in forecast.iterrows():

        if warning_date is None and row['yhat'] >= warning:
            warning_date = row['ds']

        if critical_date is None and row['yhat'] >= critical:
            critical_date = row['ds']

    results.append({
        "DATABASE": db,
        "TABLESPACE": ts,
        "WARNING_DATE": warning_date,
        "CRITICAL_DATE": critical_date
    })

# ------------------------------------
# Final Output
# ------------------------------------

result_df = pd.DataFrame(results)

print(result_df)

# Save output
result_df.to_csv("tablespace_capacity_prediction.csv", index=False)