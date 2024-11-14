import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.title("UFC Fight Outcomes Analysis")
    
    # File upload
    st.header("Upload UFC Fight Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the data
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.header("Raw Data")
        st.dataframe(df)
        
        # Calculate percentages
        for column in ['(T)KOs', 'Submissions', 'Total Decisions', 'No Contests', 'DQs']:
            df[f'{column}_Pct'] = (df[column] / df['Total Fights'] * 100).round(1)
        
        # Create a long format dataframe for visualization
        df_long = pd.melt(
            df,
            id_vars=['Division', 'Total Fights'],
            value_vars=['(T)KOs_Pct', 'Submissions_Pct', 'Total Decisions_Pct'],
            var_name='Outcome',
            value_name='Percentage'
        )
        df_long['Outcome'] = df_long['Outcome'].str.replace('_Pct', '')
        
        # Visualization 1: Stacked Bar Chart
        st.header("Fight Outcomes by Weight Class")
        chart1 = alt.Chart(df_long).mark_bar().encode(
            x=alt.X('Division:N', sort='-y'),
            y=alt.Y('Percentage:Q', stack='normalize'),
            color=alt.Color('Outcome:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Division', 'Outcome', 'Percentage']
        ).properties(
            height=400
        )
        st.altair_chart(chart1, use_container_width=True)
        
        # Visualization 2: Total Fights
        st.header("Total Fights by Weight Class")
        chart2 = alt.Chart(df).mark_bar().encode(
            x=alt.X('Division:N', sort='-y'),
            y='Total Fights:Q',
            color=alt.Color('Total Fights:Q', scale=alt.Scale(scheme='viridis')),
            tooltip=['Division', 'Total Fights']
        ).properties(
            height=400
        )
        st.altair_chart(chart2, use_container_width=True)
        
        # Detailed Statistics
        st.header("Detailed Statistics by Weight Class")
        selected_division = st.selectbox(
            "Select Weight Class",
            df['Division'].tolist()
        )
        
        div_data = df[df['Division'] == selected_division].iloc[0]
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("KO/TKO Rate", f"{div_data['(T)KOs_Pct']:.1f}%")
        with col2:
            st.metric("Submission Rate", f"{div_data['Submissions_Pct']:.1f}%")
        with col3:
            st.metric("Decision Rate", f"{div_data['Total Decisions_Pct']:.1f}%")
        with col4:
            other_pct = (div_data['No Contests_Pct'] + div_data['DQs_Pct']).round(1)
            st.metric("Other Rate", f"{other_pct:.1f}%")
        
        # Distribution chart for selected division
        st.subheader(f"Outcome Distribution for {selected_division}")
        selected_data = pd.DataFrame({
            'Outcome': ['KO/TKO', 'Submission', 'Decision', 'Other'],
            'Count': [
                div_data['(T)KOs'],
                div_data['Submissions'],
                div_data['Total Decisions'],
                div_data['No Contests'] + div_data['DQs']
            ]
        })
        
        chart3 = alt.Chart(selected_data).mark_arc().encode(
            theta='Count:Q',
            color=alt.Color('Outcome:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Outcome', 'Count']
        ).properties(
            width=400,
            height=400
        )
        st.altair_chart(chart3, use_container_width=True)

if __name__ == "__main__":
    main()
