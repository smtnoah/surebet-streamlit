
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_surebet(odds, total_stake):
    inv_total = sum(1 / o for o in odds)
    if inv_total >= 1:
        return None  # keine Surebet

    stakes = [(1 / o) / inv_total * total_stake for o in odds]
    payouts = [s * o for s, o in zip(stakes, odds)]
    profit = min(payouts) - total_stake
    yield_percent = (profit / total_stake) * 100

    return stakes, profit, yield_percent

st.set_page_config(page_title="Surebet Pro Rechner", layout="centered")
st.title("💼 Surebet Pro Rechner")
st.markdown("Berechne risikofreie Wetten inkl. 1X2 und historischem Vergleich.")

bet_type = st.selectbox("Wettart wählen:", ["2-Wege (z.B. Tennis)", "3-Wege (1X2, z.B. Fußball)"])
num_outcomes = 2 if bet_type == "2-Wege (z.B. Tennis)" else 3

odds = []
for i in range(num_outcomes):
    label = ["1", "X", "2"][i] if num_outcomes == 3 else f"Ausgang {i+1}"
    odds.append(st.number_input(f"Quote für {label}", min_value=1.01, step=0.01, format="%.2f"))

total_stake = st.number_input("Gesamteinsatz (€)", min_value=1.0, value=100.0)

if st.button("🔍 Berechnen"):
    result = calculate_surebet(odds, total_stake)

    if result:
        stakes, profit, yield_percent = result
        st.success("✅ Surebet gefunden!")

        outcome_labels = ["1", "X", "2"][:num_outcomes] if num_outcomes == 3 else [f"A{i+1}" for i in range(num_outcomes)]

        for i, s in enumerate(stakes):
            st.write(f"👉 Einsatz auf **{outcome_labels[i]}**: **{s:.2f} €**")

        st.write(f"💰 **Sicherer Gewinn:** {profit:.2f} €")
        st.write(f"📈 **Rendite:** {yield_percent:.2f} %")

        fig, ax = plt.subplots()
        ax.bar(outcome_labels, stakes, color="skyblue")
        ax.set_title("Einsatzverteilung")
        st.pyplot(fig)
    else:
        st.error("❌ Keine Surebet – die Quoten ergeben keine Arbitrage-Möglichkeit.")

st.markdown("---")
st.subheader("📂 Historische Quotenanalyse (CSV)")

uploaded_file = st.file_uploader("CSV hochladen (Spalten: Quote1, Quote2, Quote3)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    result_rows = []
    for i, row in df.iterrows():
        quotes = row.dropna().values.tolist()
        res = calculate_surebet(quotes, total_stake)
        if res:
            _, profit, yield_percent = res
            result_rows.append({'Zeile': i + 1, 'Profit (€)': round(profit, 2), 'Yield (%)': round(yield_percent, 2)})

    result_df = pd.DataFrame(result_rows)
    st.subheader("✅ Gefundene historische Surebets:")
    st.dataframe(result_df)

    fig, ax = plt.subplots()
    ax.plot(result_df['Zeile'], result_df['Yield (%)'], marker='o', linestyle='-', color='green')
    ax.set_title("📊 Historische Surebet-Renditen")
    ax.set_xlabel("Zeile")
    ax.set_ylabel("Yield (%)")
    st.pyplot(fig)
