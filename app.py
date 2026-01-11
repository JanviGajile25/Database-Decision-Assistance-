"""
Database Decision Assistant - Streamlit Application
Interactive UI for database selection decision support
"""

import streamlit as st
from decision_engine import DecisionEngine


# Page configuration
st.set_page_config(
    page_title="Database Decision Assistant",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .database-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        background-color: white;
    }
    .winner-card {
        border-color: #4CAF50 !important;
        box-shadow: 0 4px 6px rgba(76, 175, 80, 0.2);
    }
    .pros-section {
        color: #4CAF50;
        font-weight: bold;
    }
    .cons-section {
        color: #f44336;
        font-weight: bold;
    }
    .tradeoff-box {
        padding: 1rem;
        border-left: 4px solid #ff9800;
        background-color: #fff3e0;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .alternative-box {
        padding: 1rem;
        border-left: 4px solid #2196F3;
        background-color: #e3f2fd;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .score-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<p class="main-header">🗄️ Database Decision Assistant</p>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Make informed database choices with expert guidance and trade-off analysis</p>', 
                unsafe_allow_html=True)
    
    # Initialize decision engine
    if 'engine' not in st.session_state:
        st.session_state.engine = DecisionEngine()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📋 Your Requirements")
        st.markdown("---")
        
        # Application Type
        app_type = st.radio(
            "⚡ Application Type",
            options=['Web', 'Analytics', 'Real-time'],
            help="Select the primary type of your application"
        )
        
        st.markdown("---")
        
        # Data Structure
        data_structure = st.radio(
            "📊 Data Structure",
            options=['Structured', 'Semi-structured', 'Unstructured'],
            help="How is your data organized?"
        )
        
        st.markdown("---")
        
        # Scalability
        scalability = st.radio(
            "📈 Scalability Requirement",
            options=['Low', 'Medium', 'High'],
            help="Expected growth and load requirements"
        )
        
        st.markdown("---")
        
        # Transactions
        transactions = st.radio(
            "🔒 Transaction Requirement",
            options=['Low', 'High'],
            help="Need for ACID compliance and complex transactions"
        )
        
        st.markdown("---")
        
        # Schema Flexibility
        schema_flexibility = st.radio(
            "🔧 Schema Flexibility Needed",
            options=['Yes', 'No'],
            help="Do you need to change data structure frequently?"
        )
        
        st.markdown("---")
        
        # Analyze button
        analyze_button = st.button("🔍 Analyze & Compare", type="primary", use_container_width=True)
    
    # Main content area
    if analyze_button:
        # Prepare user inputs
        user_inputs = {
            'app_type': app_type,
            'data_structure': data_structure,
            'scalability': scalability,
            'transactions': transactions,
            'schema_flexibility': schema_flexibility
        }
        
        # Run analysis
        with st.spinner('Analyzing your requirements...'):
            results = st.session_state.engine.analyze(user_inputs)
        
        # Store results in session state
        st.session_state.results = results
        st.session_state.user_inputs = user_inputs
    
    # Display results if available
    if 'results' in st.session_state:
        results = st.session_state.results
        
        # Recommendation Section
        st.markdown("## 🎯 Recommendation")
        rec = results['recommendation']
        
        st.markdown(f"""
            <div class="recommendation-box">
                <h2>✅ Recommended: {rec.database}</h2>
                <p><strong>Confidence Level:</strong> {rec.confidence}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Reasoning")
        for reason in rec.reasoning:
            st.markdown(f"• {reason}")
        
        st.markdown("---")
        
        # Database Comparison
        st.markdown("## 📊 Detailed Database Comparison")
        
        cols = st.columns(3)
        
        for idx, profile in enumerate(results['profiles']):
            with cols[idx]:
                # Determine if winner
                is_winner = idx == 0
                card_class = "database-card winner-card" if is_winner else "database-card"
                
                st.markdown(f"""
                    <div class="{card_class}">
                        <h3>{profile.name} 
                        <span class="score-badge">Score: {profile.score}</span>
                        </h3>
                        <p style="color: #666;">{profile.db_type}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Pros
                st.markdown('<p class="pros-section">✅ Pros</p>', unsafe_allow_html=True)
                for pro in profile.pros:
                    st.markdown(f"• {pro}")
                
                st.markdown("")
                
                # Cons
                st.markdown('<p class="cons-section">❌ Cons</p>', unsafe_allow_html=True)
                for con in profile.cons:
                    st.markdown(f"• {con}")
        
        st.markdown("---")
        
        # Trade-offs Section
        if results['tradeoffs']:
            st.markdown("## ⚖️ Key Trade-offs to Consider")
            
            for tradeoff in results['tradeoffs']:
                st.markdown(f"""
                    <div class="tradeoff-box">
                        <h4>⚠️ {tradeoff.title}</h4>
                        <p>{tradeoff.description}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Alternatives Section
        if results['alternatives']:
            st.markdown("## 🔄 Consider These Alternatives")
            st.markdown("For specialized use cases, these databases might be better suited:")
            
            for alt in results['alternatives']:
                st.markdown(f"""
                    <div class="alternative-box">
                        <h4>💡 {alt.database}</h4>
                        <p>{alt.reason}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Technical Details Expander
        with st.expander("📈 View Detailed Scoring Breakdown"):
            st.markdown("### Score Distribution")
            
            scores_data = results['scores']
            score_df = {
                'Database': ['MySQL', 'PostgreSQL', 'MongoDB'],
                'Total Score': [scores_data['mysql'], scores_data['postgresql'], scores_data['mongodb']]
            }
            
            st.bar_chart(data=score_df, x='Database', y='Total Score')
            
            st.markdown("### Scoring Criteria")
            st.markdown(f"""
            - **Application Type:** {st.session_state.user_inputs['app_type']}
            - **Data Structure:** {st.session_state.user_inputs['data_structure']}
            - **Scalability:** {st.session_state.user_inputs['scalability']}
            - **Transactions:** {st.session_state.user_inputs['transactions']}
            - **Schema Flexibility:** {st.session_state.user_inputs['schema_flexibility']}
            """)
        
        # Export button
        st.markdown("---")
        if st.button("📥 Export Analysis Report"):
            report = generate_text_report(results, st.session_state.user_inputs)
            st.download_button(
                label="Download Report",
                data=report,
                file_name="database_decision_report.txt",
                mime="text/plain"
            )
    
    else:
        # Welcome message when no analysis has been run
        st.info("👈 Select your requirements from the sidebar and click 'Analyze & Compare' to get started!")
        
        st.markdown("### How It Works")
        st.markdown("""
        1. **Select your requirements** from the sidebar options
        2. **Click 'Analyze & Compare'** to run the decision engine
        3. **Review the recommendation** with detailed reasoning
        4. **Compare all three databases** side-by-side with pros and cons
        5. **Understand key trade-offs** in your specific context
        6. **Explore alternatives** for specialized use cases
        """)
        
        st.markdown("### What You'll Get")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎯 Smart Recommendation")
            st.markdown("Get a data-driven recommendation with confidence level and clear reasoning")
        
        with col2:
            st.markdown("#### 📊 Complete Comparison")
            st.markdown("Compare MySQL, PostgreSQL, and MongoDB with detailed pros and cons")
        
        with col3:
            st.markdown("#### ⚖️ Trade-off Analysis")
            st.markdown("Understand the trade-offs specific to your requirements")


def generate_text_report(results, user_inputs):
    """Generate a text report for export"""
    
    report = []
    report.append("=" * 70)
    report.append("DATABASE DECISION ASSISTANT - ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("")
    
    report.append("USER REQUIREMENTS:")
    report.append("-" * 70)
    report.append(f"Application Type: {user_inputs['app_type']}")
    report.append(f"Data Structure: {user_inputs['data_structure']}")
    report.append(f"Scalability: {user_inputs['scalability']}")
    report.append(f"Transactions: {user_inputs['transactions']}")
    report.append(f"Schema Flexibility: {user_inputs['schema_flexibility']}")
    report.append("")
    
    report.append("RECOMMENDATION:")
    report.append("-" * 70)
    rec = results['recommendation']
    report.append(f"Database: {rec.database}")
    report.append(f"Confidence: {rec.confidence}")
    report.append("")
    report.append("Reasoning:")
    for reason in rec.reasoning:
        report.append(f"  • {reason}")
    report.append("")
    
    report.append("DATABASE COMPARISON:")
    report.append("-" * 70)
    for profile in results['profiles']:
        report.append(f"\n{profile.name} (Score: {profile.score})")
        report.append(f"Type: {profile.db_type}")
        report.append("\nPros:")
        for pro in profile.pros:
            report.append(f"  ✓ {pro}")
        report.append("\nCons:")
        for con in profile.cons:
            report.append(f"  ✗ {con}")
        report.append("")
    
    if results['tradeoffs']:
        report.append("KEY TRADE-OFFS:")
        report.append("-" * 70)
        for tradeoff in results['tradeoffs']:
            report.append(f"\n{tradeoff.title}")
            report.append(f"  {tradeoff.description}")
        report.append("")
    
    if results['alternatives']:
        report.append("ALTERNATIVE DATABASES:")
        report.append("-" * 70)
        for alt in results['alternatives']:
            report.append(f"\n{alt.database}")
            report.append(f"  {alt.reason}")
        report.append("")
    
    report.append("=" * 70)
    report.append("End of Report")
    report.append("=" * 70)
    
    return "\n".join(report)


if __name__ == '__main__':
    main()
