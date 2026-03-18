import streamlit as st
import math
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Page config
st.set_page_config(
    page_title="Viral Titer Toolkit",
    page_icon="🦠",
    layout="centered"
)

# Initialize session state for calculation history
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []

# Initialize dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Dark mode toggle in sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
    
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    # Apply dark mode CSS
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input {
            background-color: #262730;
            color: #FAFAFA;
        }
        .stMarkdown {
            color: #FAFAFA;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Calculation History Section
    st.markdown("### 📊 Calculation History")
    
    if len(st.session_state.calculation_history) > 0:
        st.write(f"**Total Calculations:** {len(st.session_state.calculation_history)}")
        
        # Export history as CSV
        if st.button("📥 Export History (CSV)", use_container_width=True):
            # Create DataFrame from history
            df = pd.DataFrame(st.session_state.calculation_history)
            
            # Convert to CSV
            csv = df.to_csv(index=False)
            
            # Download button
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"titer_calculations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.calculation_history = []
            st.success("History cleared!")
            st.rerun()
        
        # Show recent calculations
        with st.expander("View Recent Calculations"):
            recent = st.session_state.calculation_history[-5:][::-1]  # Last 5, reversed
            for i, calc in enumerate(recent):
                st.text(f"{i+1}. {calc.get('type', 'N/A')} - {calc.get('result', 'N/A')}")
    else:
        st.info("No calculations yet")

# Title and description
st.title("🦠 Viral Titer Toolkit")
st.markdown("Professional calculators for virology research workflows")

# Create tabs for different calculators
tab1, tab2, tab3 = st.tabs(["🧮 PFU Calculator", "🔄 Reverse Calculator", "🧬 TCID50 Calculator"])

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
        
        # Save to calculation history
        st.session_state.calculation_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'PFU',
            'plaques': plaques,
            'dilution': f"10^-{exponent}",
            'volume_ul': volume,
            'result': titer_display,
            'cell_line': cell_line,
            'countability': 'Valid' if 30 <= plaques <= 300 else 'Warning'
        })
        
        # Copy and Export buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📋 Copy Titer", key="copy_titer", use_container_width=True):
                st.code(titer_display, language=None)
                st.success("✓ Copy from box above")
        
        with col_btn2:
            # Generate PDF report
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#006400'),
                spaceAfter=30,
            )
            story.append(Paragraph("PFU Titer Calculation Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Results
            story.append(Paragraph(f"<b>Viral Titer:</b> {titer_display}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Input data table
            data = [
                ['Parameter', 'Value'],
                ['Plaques Counted', str(plaques)],
                ['Dilution Factor', f"10^-{exponent}"],
                ['Volume Plated', f"{volume:.0f} µL"],
                ['Cell Line', cell_line],
                ['Incubation Time', f"{incubation_days} days"],
                ['Replicates', str(replicates)],
                ['Plate Type', plate_type],
                ['Overlay', overlay_type]
            ]
            
            table = Table(data, colWidths=[2.5*inch, 3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.3*inch))
            
            # Methods section
            story.append(Paragraph("<b>Methods:</b>", styles['Heading2']))
            story.append(Paragraph(methods_text, styles['Normal']))
            
            # Footer
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))
            
            doc.build(story)
            pdf_buffer.seek(0)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"PFU_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
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
# TAB 2: REVERSE CALCULATOR
# ============================================================================
with tab2:
    st.header("🔄 Reverse Calculator")
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
        
        # Save to calculation history
        st.session_state.calculation_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Reverse/Dilution',
            'stock_titer': f"{stock_titer_mantissa:.2f} × 10^{stock_titer_exponent}",
            'target_pfu': f"{target_pfu_mantissa:.2f} × 10^{target_pfu_exponent}",
            'result': f"{volume_needed_ul:.2f} µL",
            'pipettable': 'Yes' if 1 <= volume_needed_ul <= 1000 else 'No'
        })
        
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
# TAB 3: TCID50 CALCULATOR
# ============================================================================
with tab3:
    st.header("🧬 TCID50 Calculator")
    st.markdown("Calculate 50% Tissue Culture Infectious Dose using Reed-Muench or Spearman-Karber methods")
    
    # Method selection
    calculation_method = st.radio(
        "Calculation Method",
        options=["Reed-Muench", "Spearman-Karber"],
        horizontal=True,
        help="Reed-Muench: Most common method. Spearman-Karber: Better for incomplete data"
    )
    
    # Input section
    st.subheader("Dilution Series Data")
    
    # Number of dilutions
    num_dilutions = st.number_input(
        "Number of Dilutions Tested",
        min_value=3,
        max_value=10,
        value=6,
        step=1,
        help="Minimum 3 dilutions required for accurate calculation",
        key="tcid_num_dilutions"
    )
    
    # Initialize session state for dilution data
    if 'dilution_data' not in st.session_state:
        st.session_state.dilution_data = []
    
    # Create dynamic input table
    st.markdown("**Enter data for each dilution:**")
    
    # Table headers
    col_h1, col_h2, col_h3, col_h4 = st.columns([2, 2, 2, 2])
    with col_h1:
        st.markdown("**Dilution**")
    with col_h2:
        st.markdown("**Positive Wells**")
    with col_h3:
        st.markdown("**Total Wells**")
    with col_h4:
        st.markdown("**% Positive**")
    
    # Store dilution data
    dilution_data = []
    
    for i in range(num_dilutions):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            dilution_exp = st.selectbox(
                f"Dilution {i+1}",
                options=list(range(-1, -11, -1)),
                index=i if i < 9 else 9,
                format_func=lambda x: f"10^{x}",
                key=f"tcid_dilution_{i}",
                label_visibility="collapsed"
            )
        
        with col2:
            positive = st.number_input(
                f"Positive {i+1}",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key=f"tcid_positive_{i}",
                label_visibility="collapsed"
            )
        
        with col3:
            total = st.number_input(
                f"Total {i+1}",
                min_value=1,
                max_value=100,
                value=4,
                step=1,
                key=f"tcid_total_{i}",
                label_visibility="collapsed"
            )
        
        with col4:
            if total > 0:
                percent_positive = (positive / total) * 100
                st.metric("", f"{percent_positive:.1f}%", label_visibility="collapsed")
            else:
                st.metric("", "0%", label_visibility="collapsed")
        
        dilution_data.append({
            'dilution_exp': dilution_exp,
            'dilution_factor': 10 ** abs(dilution_exp),
            'positive': positive,
            'total': total,
            'percent': (positive / total * 100) if total > 0 else 0
        })
    
    # Additional parameters
    st.subheader("Experimental Parameters")
    
    col_param1, col_param2 = st.columns(2)
    
    with col_param1:
        inoculum_volume = st.number_input(
            "Inoculum Volume (µL)",
            min_value=1.0,
            value=100.0,
            step=10.0,
            help="Volume inoculated per well",
            key="tcid_volume"
        )
    
    with col_param2:
        tcid_cell_line = st.selectbox(
            "Cell Line",
            options=["MDCK-DP", "Vero", "BHK-21", "A549", "HEK293", "HEP-2", "HeLa"],
            index=0,
            key="tcid_cell_line"
        )
    
    # Calculate button
    if st.button("Calculate TCID50", type="primary", key="tcid_calc_button"):
        
        # Validation
        valid_data = True
        error_messages = []
        
        # Check for valid data
        if all(d['positive'] == 0 for d in dilution_data):
            error_messages.append("All wells are negative. Cannot calculate TCID50.")
            valid_data = False
        
        if all(d['positive'] == d['total'] for d in dilution_data):
            error_messages.append("All wells are positive. Cannot calculate TCID50.")
            valid_data = False
        
        # Check for at least one transition
        has_transition = False
        for i in range(len(dilution_data) - 1):
            if dilution_data[i]['percent'] > 50 and dilution_data[i+1]['percent'] < 50:
                has_transition = True
                break
        
        if not has_transition and valid_data:
            st.warning("⚠️ No clear 50% transition point detected. Results may be less reliable.")
        
        if not valid_data:
            for msg in error_messages:
                st.error(f"❌ {msg}")
        else:
            st.subheader("Results")
            
            # Reed-Muench Calculation
            if calculation_method == "Reed-Muench":
                # Find dilutions above and below 50%
                above_50 = [d for d in dilution_data if d['percent'] >= 50]
                below_50 = [d for d in dilution_data if d['percent'] < 50]
                
                if above_50 and below_50:
                    # Get the dilution just above and just below 50%
                    dilution_above = max(above_50, key=lambda x: x['dilution_exp'])
                    dilution_below = min(below_50, key=lambda x: x['dilution_exp'])
                    
                    # Calculate proportionate distance
                    percent_above = dilution_above['percent']
                    percent_below = dilution_below['percent']
                    
                    proportionate_distance = (percent_above - 50) / (percent_above - percent_below)
                    
                    # Calculate TCID50 dilution
                    log_dilution = dilution_above['dilution_exp'] + proportionate_distance
                    tcid50_dilution_factor = 10 ** abs(log_dilution)
                    
                    # Calculate TCID50/mL
                    volume_ml = inoculum_volume / 1000
                    tcid50_per_ml = tcid50_dilution_factor / volume_ml
                    
                    # Display result
                    exponent = int(math.floor(math.log10(tcid50_per_ml)))
                    mantissa = tcid50_per_ml / (10 ** exponent)
                    tcid50_display = f"{mantissa:.2f} × 10^{exponent} TCID50/mL"
                    
                    st.markdown(f"### TCID50 Titer")
                    st.markdown(f"<h2 style='color: #006400; margin-top: -10px;'>{tcid50_display}</h2>", unsafe_allow_html=True)
                    
                    # PFU conversion (calculate first before saving to history)
                    pfu_equivalent = tcid50_per_ml * 0.7
                    pfu_exp = int(math.floor(math.log10(pfu_equivalent)))
                    pfu_mant = pfu_equivalent / (10 ** pfu_exp)
                    pfu_display = f"{pfu_mant:.2f} × 10^{pfu_exp} PFU/mL"
                    
                    # Save to calculation history
                    st.session_state.calculation_history.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'TCID50 (Reed-Muench)',
                        'result': tcid50_display,
                        'pfu_equivalent': pfu_display,
                        'cell_line': tcid_cell_line,
                        'num_dilutions': num_dilutions
                    })
                    
                    st.info(f"📊 **Approximate PFU equivalent:** {pfu_display} (using 0.7 conversion factor)")
                    
                    # Calculation details
                    with st.expander("📐 Calculation Details"):
                        st.markdown(f"""
                        **Reed-Muench Method:**
                        
                        - Dilution above 50%: 10^{dilution_above['dilution_exp']} ({percent_above:.1f}% positive)
                        - Dilution below 50%: 10^{dilution_below['dilution_exp']} ({percent_below:.1f}% positive)
                        - Proportionate Distance: ({percent_above:.1f} - 50) / ({percent_above:.1f} - {percent_below:.1f}) = {proportionate_distance:.4f}
                        - Log10 TCID50 dilution: {dilution_above['dilution_exp']} + {proportionate_distance:.4f} = {log_dilution:.4f}
                        - TCID50 dilution factor: 10^{abs(log_dilution):.4f} = {tcid50_dilution_factor:.2e}
                        - TCID50/mL: {tcid50_dilution_factor:.2e} / {volume_ml} mL = {tcid50_per_ml:.2e}
                        """)
                    
                    # Data table
                    with st.expander("📊 Data Summary Table"):
                        import pandas as pd
                        df = pd.DataFrame([{
                            'Dilution': f"10^{d['dilution_exp']}",
                            'Positive': d['positive'],
                            'Total': d['total'],
                            '% Positive': f"{d['percent']:.1f}%"
                        } for d in dilution_data])
                        st.dataframe(df, use_container_width=True)
                    
                else:
                    st.error("❌ Cannot calculate: No clear 50% endpoint detected")
            
            # Spearman-Karber Calculation
            else:  # Spearman-Karber
                # Sort by dilution (highest to lowest concentration)
                sorted_data = sorted(dilution_data, key=lambda x: x['dilution_exp'], reverse=True)
                
                # Calculate proportions
                proportions = [d['positive'] / d['total'] for d in sorted_data]
                
                # Calculate sum of proportions
                sum_proportions = sum(proportions)
                
                # Get lowest dilution (highest concentration)
                x0 = sorted_data[0]['dilution_exp']
                
                # Dilution factor (log spacing)
                d = 1  # Assuming 10-fold dilutions
                
                # Spearman-Karber formula: TCID50 = 10^(x0 - d(S - 0.5))
                log_tcid50 = x0 - d * (sum_proportions - 0.5)
                
                tcid50_dilution_factor = 10 ** abs(log_tcid50)
                
                # Calculate TCID50/mL
                volume_ml = inoculum_volume / 1000
                tcid50_per_ml = tcid50_dilution_factor / volume_ml
                
                # Display result
                exponent = int(math.floor(math.log10(tcid50_per_ml)))
                mantissa = tcid50_per_ml / (10 ** exponent)
                tcid50_display = f"{mantissa:.2f} × 10^{exponent} TCID50/mL"
                
                st.markdown(f"### TCID50 Titer")
                st.markdown(f"<h2 style='color: #006400; margin-top: -10px;'>{tcid50_display}</h2>", unsafe_allow_html=True)
                
                # PFU conversion (calculate first before saving to history)
                pfu_equivalent = tcid50_per_ml * 0.7
                pfu_exp = int(math.floor(math.log10(pfu_equivalent)))
                pfu_mant = pfu_equivalent / (10 ** pfu_exp)
                pfu_display = f"{pfu_mant:.2f} × 10^{pfu_exp} PFU/mL"
                
                # Save to calculation history
                st.session_state.calculation_history.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'TCID50 (Spearman-Karber)',
                    'result': tcid50_display,
                    'pfu_equivalent': pfu_display,
                    'cell_line': tcid_cell_line,
                    'num_dilutions': num_dilutions
                })
                
                st.info(f"📊 **Approximate PFU equivalent:** {pfu_display} (using 0.7 conversion factor)")
                
                # Calculation details
                with st.expander("📐 Calculation Details"):
                    st.markdown(f"""
                    **Spearman-Karber Method:**
                    
                    - Lowest dilution (x₀): 10^{x0}
                    - Dilution factor (d): {d}
                    - Sum of proportions (S): {sum_proportions:.4f}
                    - Log10 TCID50: {x0} - {d}×({sum_proportions:.4f} - 0.5) = {log_tcid50:.4f}
                    - TCID50 dilution factor: 10^{abs(log_tcid50):.4f} = {tcid50_dilution_factor:.2e}
                    - TCID50/mL: {tcid50_dilution_factor:.2e} / {volume_ml} mL = {tcid50_per_ml:.2e}
                    """)
                
                # Data table
                with st.expander("📊 Data Summary Table"):
                    import pandas as pd
                    df = pd.DataFrame([{
                        'Dilution': f"10^{d['dilution_exp']}",
                        'Positive': d['positive'],
                        'Total': d['total'],
                        'Proportion': f"{d['positive']/d['total']:.3f}",
                        '% Positive': f"{d['percent']:.1f}%"
                    } for d in sorted_data])
                    st.dataframe(df, use_container_width=True)
            
            # Methods section
            st.subheader("Methods Section")
            
            methods_text = f"""Viral titers were determined by TCID50 assay using the {calculation_method} method. {tcid_cell_line} cells were seeded in 96-well plates and incubated overnight to reach confluence. Serial 10-fold dilutions of virus stock were prepared, and {inoculum_volume:.0f} µL of each dilution was added to replicate wells ({dilution_data[0]['total']} wells per dilution). Plates were incubated at 37°C with 5% CO₂ and monitored daily for cytopathic effect (CPE). After appropriate incubation, wells were scored as positive (CPE present) or negative (no CPE). The TCID50 was calculated using the {calculation_method} method and expressed as {tcid50_display}."""
            
            st.text_area("Copy for your methods:", methods_text, height=150, key="tcid_methods_area")
            
            # Export buttons
            col_tcid1, col_tcid2 = st.columns(2)
            
            with col_tcid1:
                if st.button("📋 Copy Methods", key="tcid_copy_methods", use_container_width=True):
                    st.code(methods_text, language=None)
                    st.success("✓ Select all (Ctrl+A) and copy (Ctrl+C)")
            
            with col_tcid2:
                # Generate TCID50 PDF
                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    textColor=colors.HexColor('#006400'),
                    spaceAfter=30,
                )
                story.append(Paragraph(f"TCID50 Calculation Report ({calculation_method})", title_style))
                story.append(Spacer(1, 0.2*inch))
                
                story.append(Paragraph(f"<b>TCID50 Titer:</b> {tcid50_display}", styles['Normal']))
                story.append(Paragraph(f"<b>PFU Equivalent:</b> {pfu_display}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
                
                # Dilution data table
                table_data = [['Dilution', 'Positive', 'Total', '% Positive']]
                for d in dilution_data:
                    table_data.append([
                        f"10^{d['dilution_exp']}",
                        str(d['positive']),
                        str(d['total']),
                        f"{d['percent']:.1f}%"
                    ])
                
                table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
                ]))
                
                story.append(table)
                story.append(Spacer(1, 0.3*inch))
                
                story.append(Paragraph("<b>Methods:</b>", styles['Heading2']))
                story.append(Paragraph(methods_text, styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))
                
                doc.build(story)
                pdf_buffer.seek(0)
                
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"TCID50_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="tcid_pdf_download"
                )
    
    # Example data button
    st.markdown("---")
    if st.button("📝 Load Example Data", key="tcid_example"):
        st.info("""
        **Example loaded!** Modify the values above to match your data.
        
        Example shows a typical influenza TCID50 assay with:
        - 6 dilutions (10⁻² to 10⁻⁷)
        - 4 wells per dilution
        - Clear 50% endpoint around 10⁻⁵
        """)

# Footer
st.markdown("---")
st.markdown("*Developed for streamlining virology workflows | Created by Tobi Olanipekun*")
