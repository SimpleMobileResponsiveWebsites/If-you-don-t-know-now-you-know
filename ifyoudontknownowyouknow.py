import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.title("UFC Fight Outcomes Analysis")
    
    # File upload
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the data
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.header("Raw Data")
        st.dataframe(df)
        
        # Calculate ratios
        df['KO_Ratio'] = df['(T)KOs'] / df['Total Fights']
        df['Submission_Ratio'] = df['Submissions'] / df['Total Fights']
        df['Decision_Ratio'] = df['Total Decisions'] / df['Total Fights']
        df['Other_Ratio'] = (df['No Contests'] + df['DQs']) / df['Total Fights']
        
        # Visualization 1: Stacked Bar Chart of Outcome Ratios
        st.header("Fight Outcome Ratios by Weight Class")
        fig1 = go.Figure()
        
        fig1.add_trace(go.Bar(
            name='KO/TKO',
            x=df['Division'],
            y=df['KO_Ratio'],
            marker_color='#ff4444'
        ))
        fig1.add_trace(go.Bar(
            name='Submission',
            x=df['Division'],
            y=df['Submission_Ratio'],
            marker_color='#33b5e5'
        ))
        fig1.add_trace(go.Bar(
            name='Decision',
            x=df['Division'],
            y=df['Decision_Ratio'],
            marker_color='#00C851'
        ))
        fig1.add_trace(go.Bar(
            name='Other (NC/DQ)',
            x=df['Division'],
            y=df['Other_Ratio'],
            marker_color='#ffbb33'
        ))
        
        fig1.update_layout(
            barmode='stack',
            xaxis_tickangle=-45,
            height=600,
            yaxis_title="Ratio of Outcomes",
            xaxis_title="Weight Class"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Visualization 2: Total Fights by Division
        st.header("Total Fights by Weight Class")
        fig2 = px.bar(
            df,
            x='Division',
            y='Total Fights',
            color='Total Fights',
            labels={'Total Fights': 'Number of Fights'},
            height=500
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed Statistics
        st.header("Detailed Statistics by Weight Class")
        selected_division = st.selectbox(
            "Select Weight Class",
            df['Division'].tolist()
        )
        
        div_data = df[df['Division'] == selected_division].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("KO/TKO Rate", f"{div_data['KO_Ratio']:.1%}")
        with col2:
            st.metric("Submission Rate", f"{div_data['Submission_Ratio']:.1%}")
        with col3:
            st.metric("Decision Rate", f"{div_data['Decision_Ratio']:.1%}")
        with col4:
            st.metric("Other Rate", f"{div_data['Other_Ratio']:.1%}")
        
        # Pie chart for selected division
        fig3 = px.pie(
            values=[
                div_data['(T)KOs'],
                div_data['Submissions'],
                div_data['Total Decisions'],
                div_data['No Contests'] + div_data['DQs']
            ],
            names=['KO/TKO', 'Submission', 'Decision', 'Other'],
            title=f"Outcome Distribution for {selected_division}"
        )
        st.plotly_chart(fig3, use_container_width=True)

if __name__ == "__main__":
    main()
