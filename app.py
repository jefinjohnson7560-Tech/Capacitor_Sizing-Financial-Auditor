import streamlit as st
import matplotlib.pyplot as plt
import math

# Page setup
st.set_page_config(page_title="Power Factor Calculator", page_icon="⚡", layout="wide")

st.title("⚡ Electrical Power Factor Correction & Audit Tool")
st.write("Adjust parameters in the sidebar to calculate required compensation and view the power triangle.")

# Inputs on sidebar
st.sidebar.header("Input Parameters")
apparent_power_s = st.sidebar.number_input("Apparent Power (S1 in kVA)", min_value=1.0, value=20.75, step=0.5)
pf_initial = st.sidebar.slider("Initial Power Factor (PF1)", min_value=0.50, max_value=0.99, value=0.78, step=0.01)
pf_target = st.sidebar.slider("Target Power Factor (PF2)", min_value=pf_initial, max_value=1.00, value=0.98, step=0.01)

# Calculations
active_power_p = apparent_power_s * pf_initial
phi1 = math.acos(pf_initial)
q1_kvar = active_power_p * math.tan(phi1)

phi2 = math.acos(pf_target)
q2_kvar = active_power_p * math.tan(phi2)

qc_required = q1_kvar - q2_kvar

# Layout
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📊 Audit Summary")
    st.metric("Active Power (P)", f"{active_power_p:.2f} kW")
    st.metric("Initial Reactive Power (Q1)", f"{q1_kvar:.2f} kVAR")
    st.metric("Target Reactive Power (Q2)", f"{q2_kvar:.2f} kVAR")
    st.success(f"### 💡 Required Capacitor Bank: **{max(0.0, qc_required):.2f} kVAR**")

with col2:
    st.subheader("📐 Power Triangle Visualization")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Base Active Power
    ax.plot([0, active_power_p], [0, 0], 'b-', linewidth=3, label=f"Active Power (P) = {active_power_p:.2f} kW")
    
    # Initial State
    ax.plot([active_power_p, active_power_p], [0, q1_kvar], 'r--', linewidth=2, label=f"Initial Q1 = {q1_kvar:.2f} kVAR")
    ax.plot([0, active_power_p], [0, q1_kvar], 'r-', linewidth=1.5, label=f"Initial S1 (PF = {pf_initial})")
    
    # Target State
    ax.plot([active_power_p, active_power_p], [0, q2_kvar], 'g-', linewidth=3, label=f"Target Q2 = {q2_kvar:.2f} kVAR")
    ax.plot([0, active_power_p], [0, q2_kvar], 'g--', linewidth=2, label=f"Target S2 (PF = {pf_target})")
    
    ax.set_title("Power Factor Correction Triangle", fontweight='bold')
    ax.set_xlabel("Active Power (kW)")
    ax.set_ylabel("Reactive Power (kVAR)")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='upper left')
    plt.tight_layout()
    
    st.pyplot(fig)
