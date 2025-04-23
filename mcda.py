import streamlit as st
import pandas as pd
import numpy as np

st.title("TOPSIS Smartphone Ranking App")

st.write("""
### Enter Smartphone Data Below
Fill in the data for each smartphone and hit the "Rank Smartphones" button.
""")

# Sample input table
sample_data = {
    'Smartphone': ['A', 'B', 'C', 'D'],
    'Price': [13000, 14000, 12000, 12500],
    'Battery': [5000, 6000, 4500, 5500],
    'Camera': [50, 48, 64, 60],
    'Performance': [7, 8, 6, 9],
    'Brand Trust': [8, 7, 9, 8]
}
df_input = pd.DataFrame(sample_data)
df_user = st.data_editor(df_input, num_rows="dynamic")

if st.button("Rank Smartphones"):
    try:
        df = df_user.copy()
        df.set_index('Smartphone', inplace=True)

        weights = np.array([0.25, 0.20, 0.20, 0.20, 0.15])
        criteria_type = ['cost', 'benefit', 'benefit', 'benefit', 'benefit']

        # Normalize
        normalized = df / np.sqrt((df**2).sum())
        weighted = normalized * weights

        # Ideal best and worst
        ideal_best = []
        ideal_worst = []

        for i, crit in enumerate(criteria_type):
            if crit == 'benefit':
                ideal_best.append(weighted.iloc[:, i].max())
                ideal_worst.append(weighted.iloc[:, i].min())
            else:
                ideal_best.append(weighted.iloc[:, i].min())
                ideal_worst.append(weighted.iloc[:, i].max())

        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)

        distance_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
        distance_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

        scores = distance_worst / (distance_best + distance_worst)
        df['TOPSIS Score'] = scores
        df['Rank'] = df['TOPSIS Score'].rank(ascending=False).astype(int)

        st.success("Ranking Completed!")
        st.dataframe(df.sort_values('Rank'))

    except Exception as e:
        st.error(f"Error: {e}")
