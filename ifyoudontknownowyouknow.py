import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_stacked_bar(df):
    fig = go.Figure()
    for outcome, color in [
        ('KO_Ratio', '#ff4444'),
        ('Submission_Ratio', '#33b5e5'),
        ('Decision_Ratio', '#00C851'),
        ('Other_Ratio', '#ffbb33')
    ]:
        fig.add_trace(go.Bar(
            name=outcome.replace('_Ratio', ''),
            x=df['Division'],
            y=df[outcome],
            marker_color=color
        ))
    return fig

def main():
    st.title("UFC Fight Outcomes Analysis")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.header("Raw Data")
        st.dataframe(df)
        
        # Calculate ratios
        total_fights = df['Total Fights']
        df['KO_Ratio'] = df['(T)KOs'] / total_fights
        df['Submission_Ratio'] = df['Submissions'] / total_fights
        df['Decision_Ratio'] = df['Total Decisions'] / total_fights
        df['Other_Ratio'] = (df['No Contests'] + df['DQs']) / total_fights
        
        # Visualization 1
        st.header("Fight Outcome Ratios by Weight Class")
        fig1 = create_stacked_bar(df)
        fig1.update_layout(
            barmode='stack',
            xaxis_tickangle=-45,
            height=600,
            yaxis_title="Ratio of Outcomes",
            xaxis_title="Weight Class"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Visualization 2
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
        
        # Statistics section
        st.header("Detailed Statistics by Weight Class")
        selected_division = st.selectbox(
            "Select Weight Class",
            df['Division'].tolist()
        )
        
        div_data = df[df['Division'] == selected_division].iloc[0]
        
        # Display metrics
        cols = st.columns(4)
        metrics = [
            ("KO/TKO Rate", div_data['KO_Ratio']),
            ("Submission Rate", div_data['Submission_Ratio']),
            ("Decision Rate", div_data['Decision_Ratio']),
            ("Other Rate", div_data['Other_Ratio'])
        ]
        
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.metric(label, f"{value:.1%}")
        
        # Pie chart
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
