import plotly.express as px
import plotly.graph_objects as go

def create_visualizations(df):
    figs = []
    
    # Meetings per day
    fig_meetings_per_day = px.bar(
        df.groupby(df['start'].dt.date).size().reset_index(name='count'),
        x='start',
        y='count',
        title='Meetings per Day'
    )
    figs.append(fig_meetings_per_day)
    
    # Meeting duration distribution
    fig_duration_dist = px.histogram(
        df,
        x='duration',
        title='Meeting Duration Distribution',
        labels={'duration': 'Duration (hours)'}
    )
    figs.append(fig_duration_dist)
    
    # Attendees distribution
    fig_attendees_dist = px.histogram(
        df,
        x='attendees',
        title='Meeting Attendees Distribution'
    )
    figs.append(fig_attendees_dist)
    
    # Time of day distribution
    df['hour'] = df['start'].dt.hour
    fig_time_dist = px.histogram(
        df,
        x='hour',
        title='Meeting Time Distribution',
        labels={'hour': 'Hour of Day'}
    )
    figs.append(fig_time_dist)
    
    # Meeting duration vs. Attendees scatter plot
    fig_duration_vs_attendees = px.scatter(
        df,
        x='duration',
        y='attendees',
        title='Meeting Duration vs. Number of Attendees',
        labels={'duration': 'Duration (hours)', 'attendees': 'Number of Attendees'}
    )
    figs.append(fig_duration_vs_attendees)
    
    # Meetings by category
    fig_meetings_by_category = px.pie(
        df,
        names='category',
        title='Distribution of Meetings by Category'
    )
    figs.append(fig_meetings_by_category)
    
    # Duration by category
    fig_duration_by_category = px.bar(
        df.groupby('category')['duration'].sum().reset_index(),
        x='category',
        y='duration',
        title='Total Duration of Meetings by Category',
        labels={'duration': 'Total Duration (hours)'}
    )
    figs.append(fig_duration_by_category)
    
    return figs
