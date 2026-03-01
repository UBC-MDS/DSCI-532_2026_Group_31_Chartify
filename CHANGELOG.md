## [0.2.0] - 2026-03-01

### Added

- Scatter plot grid showing all audio features vs. selected metric, with line of best fit per subplot
- Chartify brand styling: Spotify green (`#1DB954`) card outlines, table headers, and sidebar border
- Circular Std / Helvetica font applied across the dashboard
- Dark sidebar background (`#111111`) with green border separator
- Metrics cards displaying average feature counts
- Dropdown menus to select a metric of interest and an artist
- Clickable choice box to select platform(s) of interest
- Top 5 songs table for artist of choice

### Changed

- From the original sketch with one scatterplot (and all features graphed on it), changed to using a scatterplot grid for Milestone 2 instead. This is due the the single-plot method not working and/or being unreadable.
- The layout of the dashboard has changed from milestone 1 -> 2. It has been significantly minimized due to current time constraints. More information found in the "Layout Changes" section in the Reflection below.

### Fixed

N/A, this is the first deployed iteration

### Known Issues

- X-axis labels on scatter subplots can overlap at smaller window sizes
- Value boxes may show `NaN` if artist has no data for a given metric

### Reflection

**Implementation Status**: Core filtering, summary cards, top 5 table, and scatter plot grid are all functional and deployed on Posit Cloud.

#### Job Stories Status

- **Fully Implemented**: #1, (platform and artist filter, avg. metric cards), #2 (top 5 songs table, avg. metric cards), #3 (scatter plot of audio features vs. metric)
- **Partially/Mostly Done**: -None-
- **Pending M3**: all -> just for further improvements

#### Layout Changes:

The following sketched visuals from Milestone 1 have not been implemented due to time constraints:
 - "Platform and Licensed breakdown"
 - "Singles %%" & "Albums %%"
 - "Song Duration (Avg)"
 - Bar chart of song features (Energy, Loudness, Speechiness etc.)
 - "Song Scope" and "Licensed" radio button filters
 - "Song Feature(s)" dropdown/Search box + Slider
 - "Metric of interest" dropdown/Search box.

These may or may not be incorporated in further future developments.

**Deviations from Plan**: Switched from Plotly to Matplotlib for the scatter plot due to `shinywidgets` incompatibility with the Posit Cloud Shiny version. The original plan called for a single overlaid scatter plot; this was changed to a grid of subplots per feature for clarity.

**Design Rationale**: Chartify brand colors and fonts were applied to align the dashboard with the project identity. Green outlines and dark backgrounds follow the Spotify-inspired palette from the brand guide, and the colours were taken from Spotify's 2023 Wrapped Palette.

**Visualization Best Practices**: Each audio feature is plotted independently to avoid scale distortion. A line of best fit is included per subplot to surface directional trends. X-axis is formatted in human-readable millions.

**Strengths**: Dashboard is responsive to artist and platform filters. Styling is consistent and on-brand. Scatter plot provides feature-level insight per song.

**Limitations**: Small number of data points per artist limits the interpretability of the lines of best fit. Scatter plots are static (no hover/tooltip in matplotlib).

**Future Improvements**: Add interactivity back to scatter plot (e.g. Plotly once shinywidgets compatibility is resolved). Add artist search suggestions/autocomplete. Surface tooltip with song name on hover. Additional components and visualizations such as a bar chart to display the average song feature metrics by artist searched.
