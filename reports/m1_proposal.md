# Chartify: Spotify Dashboard Analytics

## Section 1: Motivation and Purpose

**Our Role**: Data Scientists at Spotify

Music is universal. It has the ability to transcend language, age & culture to reach audiences from all corners of the globe. More importantly, music has the ability to stimulate the mind and alter your brain chemistry. Needless to say, understanding the qualities of "good" music is an important need for anyone in the music industry.

As Data Scientists at Spotify, we aim to utilize Spotify's unique song attributes such as Acousticness, Valence, Tempo etc to create a dashboard that visualizes the qualities of "good" music. We are using song popularity as the analogy for "good" music. We see the application of our dashboard to a variety of audiences. For example, this dashboard can be used by music artists and producers to understand what song attributes resonate the most with listeners. This information can be used to refine the musical journey by adjusting the song's respective attributes. As well, given our dataset contains a feature `most_playedon` describing what platform listened to the songs most, we aim to use this as a differentiating attribute to understand how songs perform on different platforms.

## Section 2: Description of the Data

We will be visualizing a dataset of 20594 music tracks originally retrieved from the Spotify Web API (deprecated) and compiled by Sanjana Chaudhari (2023) found [here](https://www.kaggle.com/datasets/sanjanchaudhari/spotify-dataset/data). Each track has 24 associated features which we have categorized into the following:

- Metadata and identification: Artist, Track, Album, Album_type, Title
- Acoustic profile: Danceability, Energy, Loudness, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, EnergyLiveness
- Technical song attributes: Tempo, Duration
- Engagement metrics: views, Likes, Comments, Stream, most_playedon
- Distribution contexts: Channel, Licensed, official_video

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario:

Jane, a music producer at UMG, is planning on creating a new single for an up and coming music artist. The main goals with this song are to chart well and have listening longevity for fans of this artist AND naive listeners. This balance between popularity and longevity across both fans and casual listeners is very difficult to find, especially with how fast paced the industry trends are. Jane needs help with deciding on the direction of this new single and would like information on features that perform well, such as genre and song attributes to get her started. As a bonus, she would appreciate information on how this may or may not differ on different platforms such as Spotify (auditory) and Youtube (has visual elements, which may affect the listening/viewership experience).

When Jane uses Chartify, she can see how different song elements and audio features affect popularity using Spotify's full feature set, and filter for specific attributes to understand how feature interactions influence a song's reception. YouTube performance metrics (likes, comments, views) are also included alongside a platform performance indicator, enabling further personalization based on her target platform. Exploring this data, Jane may, for example, notice that tracks with high valence and moderate danceability consistently over-index on YouTube engagement which will lead her to guide her single's direction around an upbeat, emotionally resonant sound built to perform across both platforms.

### User Stories:

**User Story 1**: As a _record label executive_, I want to predict which platform a song will do better in, based on selected features, in order to determine what marketing tactics are better to invest in.

**User Story 2**: As a _music producer_, I want to visualize how filtering for song elements such as danceability, tempo, or acousticness will affect song popularity (at either high or low values) in order to guide me in my songwriting process.

**User Story 3**: As a _music producer_, I want to select the most liked songs on Youtube, in order to determine which genres perform best on a video platform.

## Section 4: Exploratory Data Analysis


## Section 5: App Sketch & Description

The visual mockup of our app is shown below. It features a set of KPI summary cards at the top for the main metrics of interest (likes, comments, etc) as well as multiple perspectives from the source data. 

These multiple perspectives include: a stacked bar chart that compares platform distribution (Spotify vs YouTube) and the licensing status within each platform, a song bar chart to display the numerical feature values and compare their proportions, a tabular view that highlights the top songs and allows for easy comparison amongst them, and finally a central scatter plot that visualizes relationships between a selected performance metric and the song features. This scatter chart directly enables pattern discovery by showing where certain song clusters are with the best metric values.

Along with these main visualizations and displayed metrics, the dashboard app also includes a collapsible filter panel (with radio buttons, sliders, dropdown etc.) which allows for further filtering interactions and updates reactively based on user selections.

![Sketch](../img/sketch.png)
