# AI-Powered Oracle Tablespace Growth Prediction

This project demonstrates how machine learning can be applied to Oracle database administration to proactively predict tablespace capacity risks.

Using historical monitoring data from the Oracle Enterprise Manager (OEM) repository and the Prophet time-series forecasting model, the system predicts when tablespaces will reach warning and critical thresholds.

The results are integrated into a **Streamlit-based DBA automation dashboard** to help DBAs perform proactive capacity planning.

## Dashboard Preview

### Main Dashboard
![Dashboard](screenshots/Dashboard-Mainpage.png)

### Tablespace Forecast Table
![Forecast](screenshots/Tablespace-Forecast-table.png)

The dashboard displays:

- AI-based tablespace growth prediction  
- Warning and critical threshold forecast dates  
- Risk classification for each tablespace  

## Example Prediction Output

| Database | Tablespace | Warning Date | Critical Date |
|---------|------------|--------------|---------------|
| PRODDB | SYSAUX | 2026-05-12 | 2026-06-03 |
| PRODDB | USERS | SAFE | SAFE |
| TESTDB | SYSTEM | 2026-04-18 | 2026-05-02 |

## Technologies Used

- Python
- Facebook Prophet (Time-Series Forecasting)
- Pandas
- Streamlit
- Oracle SQL
- Data Visualization
