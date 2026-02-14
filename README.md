# Group 31

### Chartify: Spotify Dashboard Analytics

Chartify is a data analytics dashboard that leverages Spotify's song features dataset to uncover patterns and characteristics of successful songs. Built for music producers and A&R professionals, it provides actionable insights on tempo, energy, danceability, and other key metrics that correlate with chart performance and cross-platform popularity, helping stakeholders make data-driven decisions in hit song production.

## Installation

To install the required packages and run the app locally, copy and paste the following code into your terminal.

```bash
# After opening a terminal:
git clone https://github.com/UBC-MDS/DSCI-532_2026_Group_31_Chartify.git
cd DSCI-532_2026_Group_31_Chartify/

# Optional (but suggested): make a fresh environment
conda create -n chartify python=3.11 # will install auto-pip gracefully 
conda activate chartify
pip install -r requirements.txt

# Run draft application locally  
python src/app.py # → http://127.0.0.1:8050

# Optional (but suggested): deactivate environment when done
conda deactivate
```
