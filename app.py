import streamlit as st
import math

# Page config
st.set_page_config(
    page_title="Viral Titer Calculator",
    page_icon="🦠",
    layout="centered"
)

# Title and description
st.title("🦠 Viral Titer Toolkit")
st.markdown("Professional calculators for virology research workflows")

# Create tabs for different calculators
tab1, tab2, tab3 = st.tabs(["🧮 PFU Calculator", "Stock Titer Dilution Calculator", "🧬 TCID50 Calculator"])

# ============================================================================
# TAB 1: PFU TITER CALCULATOR
# ============================================================================
with tab1:
    st.header("PFU Titer Calculator")
    st.markdown("Calculate viral titers from plaque assays with automatic countability checks")
    
    # Input section
    st.subheader("Assay Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        plaques = st.number_input(
            "Plaques Counted",
            min_value=0,
            value=50,
            step=1,
            help="Number of plaques counted on the plate",
            key="pfu_plaques"
        )
    
    with col2:
        # Create dilution options from 10^-1 to 10^-9
        dilution_options = {
            "10⁻¹ (0.1)": 10,
            "10⁻² (0.01)": 100,
            "10⁻³ (0.001)": 1000,
            "10⁻⁴": 10000,
            "10⁻⁵": 100000,
            "10⁻⁶": 1000000,
            "10⁻⁷": 10000000,
            "10⁻⁸": 100000000,
            "10⁻⁹": 1000000000
        }
        
        dilution_label = st.selectbox(
            "Dilution Factor",
            options=list(dilution_options.keys()),
            index=5,  # Default to 10^-6
            help="Select the dilution used for plating",
            key="pfu_dilution"
        )
        
        dilution = dilution_options[dilution_label]
    
    with col3:
        volume = st.number_input(
            "Volume Plated (µL)",
            min_value=1.0,
            value=100.0,
            step=10.0,
            help="Volume of inoculum plated",
            key="pfu_volume"
        )
    
    # Experimental Details Section
    st.subheader("Experimental Details (for Methods)")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        cell_line = st.selectbox(
            "Cell Line",
            options=["MDCK-DP", "Vero", "BHK-21", "A549", "HEK293", "HEP-2", "HeLa"],
            index=0,  # Default to MDCK-DP
            help="Cell line used for the plaque assay",
            key="pfu_cell_line"
        )
    
    with col5:
        # Incubation time in hours (2 days = 48h to 14 days = 336h)
        incubation_options = {
            "2 days (48h)": 48,
            "3 days (72h)": 72,
            "4 days (96h)": 96,
            "5 days (120h)": 120,
            "6 days (144h)": 144,
            "7 days (168h)": 168,
            "8 days (192h)": 192,
            "9 days (216h)": 216,
            "10 days (240h)": 240,
            "11 days (264h)": 264,
            "12 days (288h)": 288,
            "13 days (312h)": 312,
            "14 days (336h)": 336
        }
        
        incubation_label = st.selectbox(
            "Incubation Time",
            options=list(incubation_options.keys()),
            index=1,  # Default to 3 days
            help="Time plates were incubated before counting",
            key="pfu_incubation"
        )
        
        incubation_hours = incubation_options[incubation_label]
        incubation_days = incubation_hours // 24
    
    with col6:
        replicates = st.selectbox(
            "Number of Replicates",
            options=[1, 2, 3, 4, 5, 6],
            index=1,  # Default to 2 replicates
            help="Number of replicate wells plated",
            key="pfu_replicates"
        )
    
    # Additional optional fields
    col7, col8 = st.columns(2)
    
    with col7:
        plate_type = st.selectbox(
            "Plate Type",
            options=["6-well plate", "12-well plate", "24-well plate", "35mm dish", "60mm dish", "100mm dish"],
            index=0,
            help="Type of culture vessel used",
            key="pfu_plate_type"
        )
    
    with col8:
        overlay_type = st.selectbox(
            "Overlay Medium",
            options=["Agar overlay", "Agarose overlay", "Methylcellulose overlay", "CMC overlay"],
            index=0,
            help="Type of overlay used to restrict viral spread",
            key="pfu_overlay"
        )
    
    # Calculate button
    if st.button("Calculate PFU/mL", type="primary", key="pfu_calc_button"):
        # Convert µL to mL
        volume_ml = volume / 1000
        
        # Calculate PFU/mL
        pfu_ml = (plaques * dilution) / volume_ml
        
        # Countability check
        st.subheader("Results")
        
        if plaques < 30:
            st.warning(f"⚠️ Plaque count ({plaques}) is below 30 - results may lack statistical reliability")
        elif plaques > 300:
            st.warning(f"⚠️ Plaque count ({plaques}) is above 300 - plate may be too confluent for accurate counting")
        else:
            st.success("✅ Plaque count is within optimal range (30-300)")
        
        # Display result with proper scientific notation and dark green color
        # Convert to scientific notation format
        if pfu_ml > 0:
            exponent = int(math.floor(math.log10(pfu_ml)))
            mantissa = pfu_ml / (10 ** exponent)
            titer_display = f"{mantissa:.2f} × 10^{exponent} PFU/mL"
        else:
            titer_display = "0 PFU/mL"
        
        st.markdown(f"### Viral Titer")
        st.markdown(f"<h2 style='color: #006400; margin-top: -10px;'>{titer_display}</h2>", unsafe_allow_html=True)
        
        # Copy button for titer
        if st.button("📋 Copy Titer", key="copy_titer"):
            st.code(titer_display, language=None)
            st.success("✓ Copied! Use Ctrl+C to copy from the box above")
        
        # Methods section
        st.subheader("Methods Section")
        
        # Calculate the exponent for better methods text
        if dilution > 1:
            exponent = int(math.log10(dilution))
        else:
            exponent = 0
        
        # Build comprehensive methods paragraph
        replicate_text = "in duplicate" if replicates == 2 else "in triplicate" if replicates == 3 else f"with {replicates} replicates" if replicates > 1 else ""
        
        methods_text = f"""Viral titers were determined by plaque assay on {cell_line} cells. Confluent cell monolayers in {plate_type}s were prepared 24 hours prior to infection. Serial 10-fold dilutions of virus stocks were prepared in infection medium, and {volume:.0f} µL of each dilution was inoculated onto the cells {replicate_text}. After 1 hour adsorption at 37°C with 5% CO₂, the inoculum was removed and cells were overlaid with {overlay_type.lower()}. Plates were incubated at 37°C with 5% CO₂ for {incubation_days} days ({incubation_hours} hours). Following incubation, cells were fixed with 4% formaldehyde and stained with 0.1% crystal violet to visualize plaques. Plaques from the 10⁻{exponent} dilution were manually counted ({plaques} plaques{' per well, averaged across replicates' if replicates > 1 else ''}), and viral titers were calculated as {titer_display}."""
        
        st.text_area("Copy for your methods:", methods_text, height=200, key="methods_text_area")
        
        # Add a copy button that shows the text in a copyable format
        col_copy1, col_copy2 = st.columns([1, 5])
        with col_copy1:
            if st.button("📋 Copy Methods", key="copy_methods"):
                st.session_state.show_methods_copy = True
        
        if st.session_state.get("show_methods_copy", False):
            st.info("✓ Select all text below (Ctrl+A) and copy (Ctrl+C)")
            st.code(methods_text, language=None)

# ============================================================================
# TAB 2: Stock Titer Dilution CALCULATOR
# ============================================================================
with tab2:
    st.header("Stock Titer Dilution Calculator")
    st.markdown("*Plan your experiment: Calculate volume needed to achieve a target PFU amount*")
    
    st.markdown("**Scenario:** You know your stock titer and need to calculate how much volume to use")
    
    col_rev1, col_rev2 = st.columns(2)
    
    with col_rev1:
        st.subheader("Known Values")
        
        # Stock titer input
        stock_titer_mantissa = st.number_input(
            "Stock Titer",
            min_value=0.1,
            max_value=9.99,
            value=5.0,
            step=0.1,
            help="The coefficient in scientific notation (e.g., 5.0 in 5.0 × 10⁸)",
            key="rev_stock_mantissa"
        )
        
        stock_titer_exponent = st.selectbox(
            "Stock Titer (exponent)",
            options=[4, 5, 6, 7, 8, 9, 10, 11, 12],
            index=4,  # Default to 10^8
            help="The exponent in scientific notation",
            key="rev_stock_exp"
        )
        
        stock_titer_pfu_ml = stock_titer_mantissa * (10 ** stock_titer_exponent)
        st.info(f"Stock Titer: {stock_titer_mantissa:.2f} × 10^{stock_titer_exponent} PFU/mL")
    
    with col_rev2:
        st.subheader("Target Amount")
        
        target_pfu_mantissa = st.number_input(
            "Target PFU",
            min_value=0.1,
            max_value=9.99,
            value=1.0,
            step=0.1,
            help="Desired number of PFU (coefficient)",
            key="rev_target_mantissa"
        )
        
        target_pfu_exponent = st.selectbox(
            "Target PFU (exponent)",
            options=[3, 4, 5, 6, 7, 8, 9, 10],
            index=3,  # Default to 10^6
            help="The exponent for target PFU",
            key="rev_target_exp"
        )
        
        target_pfu = target_pfu_mantissa * (10 ** target_pfu_exponent)
        st.info(f"Target: {target_pfu_mantissa:.2f} × 10^{target_pfu_exponent} PFU")
    
    if st.button("Calculate Volume Needed", type="primary", key="reverse_calc"):
        # Calculate volume needed in mL
        volume_needed_ml = target_pfu / stock_titer_pfu_ml
        volume_needed_ul = volume_needed_ml * 1000
        
        st.markdown("### 📋 Results")
        
        # Display results
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.metric("Volume Needed", f"{volume_needed_ul:.2f} µL")
            st.caption(f"({volume_needed_ml:.6f} mL)")
        
        with col_res2:
            # Calculate dilution factor if needed
            if volume_needed_ul > 1000:
                suggested_dilution = volume_needed_ul / 100  # Suggest diluting to use 100 µL
                st.warning(f"⚠️ Large volume needed")
                st.markdown(f"**Suggestion:** Dilute stock 1:{suggested_dilution:.0f} and use 100 µL")
            elif volume_needed_ul < 1:
                st.warning(f"⚠️ Very small volume - pipetting may be inaccurate")
                st.markdown(f"**Suggestion:** Dilute your stock or use a larger target PFU")
            else:
                st.success("✅ Volume is pipettable")
        
        # Practical recommendations
        st.markdown("### 💡 Practical Tips")
        
        if volume_needed_ul < 10:
            st.info(f"🔬 For accuracy with small volumes, consider diluting your stock {int(10/volume_needed_ul)}:1 and using {volume_needed_ul * int(10/volume_needed_ul):.1f} µL")
        
        # Show calculation details
        with st.expander("📐 Calculation Details"):
            st.markdown(f"""
            **Formula:** Volume (mL) = Target PFU / Stock Titer (PFU/mL)
            
            **Calculation:**
            - Stock Titer: {stock_titer_mantissa:.2f} × 10^{stock_titer_exponent} PFU/mL = {stock_titer_pfu_ml:.2e} PFU/mL
            - Target PFU: {target_pfu_mantissa:.2f} × 10^{target_pfu_exponent} = {target_pfu:.2e} PFU
            - Volume = {target_pfu:.2e} / {stock_titer_pfu_ml:.2e} = {volume_needed_ml:.6f} mL
            - Volume = {volume_needed_ul:.2f} µL
            """)

# ============================================================================
# TAB 3: TCID50 CALCULATOR (Placeholder)
# ============================================================================
with tab3:
    st.header("🧬 TCID50 Calculator")
    st.markdown("Calculate 50% Tissue Culture Infectious Dose using Reed-Muench or Spearman-Karber methods")
    
    st.info("🚧 TCID50 Calculator coming soon! This will support both Reed-Muench and Spearman-Karber calculations.")
    
    # Placeholder for future implementation
    st.markdown("""
    **Features will include:**
    - Reed-Muench method
    - Spearman-Karber method
    - Dynamic dilution series input
    - TCID50 to PFU conversion
    - Automated methods section generation
    """)

# Footer
st.markdown("---")
st.markdown("*Developed for streamlining virology workflows | Created by Tobi Olanipekun*")
