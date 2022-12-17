## Project Abstract

We take the preliminary results of Project 2, and we redo some of them so it's quantitative instead of qualitative analysis- and then we slap that into a OpenAPI compliant interface using FastAPI, and produce a half-baked NextJS based dashboard to showcase some of the the graphs as dashboards. Unfortunately due to time constraints, a significant portion of the functionality is still locked behind the API routes only.

## Team - Gatorade

* Jacob Barkovitch, jbarkov1@binghamton.edu
* Guy Ben-Yishai, gbenyis1@binghamton.edu
* Alan Bixby, abixby1@binghamton.edu
* Jacob Coddington, jcoddin1@binghamton.edu
* Ryan Geary, rgeary1@binghamton.edu
* Joseph Lieberman, jliebe12@binghamton.edu

## Tech-stack

* `Python 3.8` - The project is developed and tested using python v3.8; packages are managed using `poetry`, but the `pyproject.toml` *should* be fairly package manager agnostic
* `MongoDB v6.0.2` - An industry staple, [web scale](https://www.youtube.com/watch?v=HdnDXsqiPYo), NoSQL database- handles schemaless input and theres less of a concern for accidental SQL injections. [MongoDB](https://www.mongodb.com/)
* [`python-dotenv`](https://github.com/theskumar/python-dotenv) - Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. [python-dotenv repo](https://github.com/theskumar/python-dotenv)
* [`numpy`](https://numpy.org/) - a fundamental package for scientific computing with Python
* [`matplotlib`](https://matplotlib.org/) - a comprehensive library for creating static, animated, and interactive visualizations in Python
* [`seaborn`](https://seaborn.pydata.org/) - a Python data visualization library based on [matplotlib](https://matplotlib.org)
* [`fastapi`](https://fastapi.tiangolo.com/) - a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints
* [`uvicorn`](https://www.uvicorn.org/) - an ASGI web server implementation for Python, used to run `fastapi`
* [`thefuzz`](https://github.com/seatgeek/thefuzz) - used for fuzzy search of API inputs to prevent the need to memorize exact team names or subreddits
* [`scipy`](https://scipy.org/) - used for integrating the time series data to find overall sentiment scores across time

Dashboard
- [`NextJS`](https://nextjs.org/) - a flexible React framework that gives you building blocks to create fast web applications
- [`ChartJS`](https://www.chartjs.org/) - a simple yet flexible JavaScript charting library for the modern web
- [`ChartJSNextJSDashboard Github Template`](https://github.com/Princekrampah/ChartJSNextJSDashboard): a Python centric, [full stack dashboard template found on YouTube](https://www.youtube.com/watch?v=UDvhgJTWtfQ)

Minimal webscraping for extra data used, these projects will appear as branches:
- `NodeJS` - a JavaScript runtime
- `TypeScript` - the superior form of JavaScript
- [`FuseJS`](https://fusejs.io/) - a powerful, lightweight fuzzy-search library, with zero dependencies.
- [`Cheerio`](https://cheerio.js.org/) - fast, flexible & lean implementation of core jQuery designed specifically for the server.
- [`got-scraping`](https://github.com/apify/got-scraping) - an extended version of [`Got`](https://www.npmjs.com/package/got) that automatically changes user-agents, etc, to avoid rate limiting while webscraping

## Three data-sources

Our three data sources consist of the same dataset defined in [Project 1](https://github.com/2022-Fall-CS-415-515/project-1-implementation-team-gatorade/blob/master/README.md); however for computational complexity, the focus of our time was put on NFL data. There is heavy overlap between what was implemented in Project 2 and Project3. The following cleaning has been done as outlines:

### Extra NFL Data
- Team rosters were web-scraped from [`footballdb.com`](https://www.pro-football-reference.com/years/2022/games.htm) using `Cheerio` and `got-scraping`, implemented in project 2 [`roster-to-entitlementids`](https://github.com/2022-Fall-CS-415-515/project-2-implementation-team-gatorade/tree/roster-to-entitlementid)
- Game scores and durations (start/end times in EST) were fetched from the `pro-football-reference.com` data set, implemented in [`nfl-endtimes`](https://github.com/2022-Fall-CS-415-515/project-3-implementation-team-gatorade/tree/nfl-endtimes)

### Twitter
- Teams were designated for tweets by using the Twitter Entitlement IDs that matches the team name or player roster names; matches were done using a fuzzy search with `FuseJS`, to reduce the amount of missed data from nicknames/name formatting differences; in instances where more than one match was found, the strongest match was used
- See [`teamToEntitlementIds.json`](https://github.com/2022-Fall-CS-415-515/project-3-implementation-team-gatorade/blob/master/src/teamToEntitlementIds.json) for entity ID to team mappings

### Reddit
- Due to time constraints, only `subreddit` was used to map comments to a team. Unfortunately this means places like `/r/nfl` are entirely excluded from our analysis- but it was too complexity to design a ML model, etc that could accurately classify arbitrary text to a given team
- See [`teamToSubreddits.json`](https://github.com/2022-Fall-CS-415-515/project-3-implementation-team-gatorade/blob/master/src/teamToSubreddits.json) for subreddit to team mappings

### Odds API
- Only NFL data is considered; NCAAF while **very** well covered by the betting odds, had insufficient amounts of filtered player data in the Twitter and Reddit data pipelines to practically use.

---

## How to view the project?
As outlined in Project 1, a Google VM was created for slightly better specs/redundancy during an outage (using free credit!)- the demo was conducted using the Google VM, but by the time this is graded, this *should* be runnable on the school's provided VM. The only hold up for the demo was the fact that there was insufficient space to migrate the segregated data to the VM; so the analysis was needed to be computed on the full data set (in-place), which there was insufficient space to do.

#### Binghamton VM
Navigate to the following links:
- Dashboard: https://dashboard.ds.bxb.gg
- OpenAPI Docs: https://api.ds.bxb.gg
> localhost/code level access is the same as `School VM` listed below

#### Local Code Access:
```bash
ssh prod@***.***.***.*** # (Google VM)
ssh prod@***.***.***.*** # (Binghamton VM)
```
> Code should match on both machines; if not, `git pull`, with the associated SSH-key, same password as SSH.

#### School VM
1. Connect to the Ivanti VPN (formerly Pulse VPN)
3. In two separate terminals, construct SSH reverse tunnels to the VM on port 3000 (dashboard) and port 5000 (API):
	-  `ssh -L 3000:localhost:3000 -L 5000:localhost:5000 <username>@***.***.***.***`
	- I personally use `SSH Remote` on VSCode which automatically handles the remote port forwarding, so YMMV- consult the `bxb.gg` links otherwise.
4. From a local browser, access `localhost:3000` and `localhost:5000/docs`
	- This is equvialent to [`https://dashboard.ds.bxb.gg`](`https://dashboard.ds.bxb.gg`) and [`https://api.ds.bxb.gg`](`https://dashboard.ds.bxb.gg`), respectively
5. In the API Docs, expanding a route, clicking `Try it out` in the top right corner, then filling in the appropriate fields, and hitting `Execute` will process a request.

---
## From Fresh Install
1. Clone the repository and navigate into the package.
2. Initialize a new virtual environment with `poetry shell`
3. Install the Python dependencies with `poetry install`
4. Run `python src/api.py` to start the FastAPI webserver
5. Navigate to `dashboard`, run `npm install` to install NodeJS dependencies
6. Run `npm start` to start the NextJS webserver for the dashboard

> On both the Google VM and Binghamton VM, these are managed via PM2 and will already be running. Running second processes with fail/launch on a different port.

--- 
# Web Dashboard
### Accessible on https://dashboard.ds.bxb.gg (localhost:3000)

A minimal web dashboard using some of the endpoints of the API to generate data using `ChartJS`; much more functionality is available (exclusively) on the API docs page.

This dashboard was slapped together last minute from [this YT Tutorial GitHub template repo.](https://github.com/Princekrampah/ChartJSNextJSDashboard)

![image](https://user-images.githubusercontent.com/34300238/208235611-963d5193-a498-48dc-8a27-14b8310f7659.png)

> Clicking elements on the legend can hide/show data sources

--- 
# OpenAPI Documentation
### Accessible on https://api.ds.bxb.gg/docs (localhost:5000/docs)

An API for generating graphs and dataframes of sentiment analysis data for NFL teams on Reddit and Twitter 🏈

> **General note:** `Los Angeles Rams` are not supported for any Reddit data retrieval; the fact that there are two Los Angeles teams likely caused us to think one was a mistake/duplicate and it was purged from our original subreddit list for data collection.  

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/df/{team_name}/{collection}/{mode}](#getdfteam_namecollectionmode) | Generate Dataframe Data |
| GET | [/games](#getgames) | List of NFL Games |
| GET | [/most_positive/{data_source}](#getmost_positivedata_source) | Get Most Positive Team |
| GET | [/least_postive/{data_source}](#getleast_postivedata_source) | Get Least Positive Team |
| GET | [/positivity_sort/{data_source}](#getpositivity_sortdata_source) | Get Positivity Sort |
| GET | [/odds/odds_ts](#getoddsodds_ts) | Get Bookmaker Odds |
| GET | [/odds/odds_avg](#getoddsodds_avg) | Get Average Bookmaker Odds |
| GET | [/graph/odds](#getgraphodds) | Graph Betting Odds |
| GET | [/graph/team/{team_name}](#getgraphteamteam_name) | Graph Team Polarity |
| GET | [/graph/game/{game_id}](#getgraphgamegame_id) | Graph Team Vs Team Polarities |
| GET | [/diff/{game_id}](#getdiffgame_id) | Calculate Game Difference |

## 
## Path Details

***

### **[GET]** /df/{team_name}/{collection}/{mode}

Summary  
- Generate Dataframe Data

Description  
- Generate a dataframe of data for a given team, data source, and metric; allows for custom time windows  
  
- team_name: name of the team; fuzzy search enabled ("buffalo" -> "Buffalo Bills")
- collection: data source to use; reddit or twitter
- mode: metric to use; sentiment or frequency
- focus_datetime: a `datetime` to center the graph on; generally the game start time  
- window_before: a `timedelta` of the amount of time to fetch *prior* to the `focus_datetime`
- window_after: a `timedelta` of the amount of time to fetch **following** the `focus_datetime`
- sample_window: a `timedelta` template string to be used for the moving average calculation
- resample_window: a `timedelta` template string to be used for the graphing interval (otherwise every point is shown which takes *forver* to render)
- all_data: bool; override the window parameters and just graph everything

#### Parameters(Path)
```ts
team_name: string
collection: 'reddit' | 'twitter'
mode: 'sentiment'
```

#### Parameters(Query)

```ts
focus_datetime?: string // 2022-11-14T12:00:00+00:00
window_before?: number // 172800 (seconds) 
window_after?: number // 172800 (seconds)
sample_window?: string // 2D
resample_window?: string // 90T
all_data?: boolean // false
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
	polarity: number[] // [0.08553888081356927, ..., 0.07893374467957985]
	sentiment: number[] // [0.4102488992935106, ..., 0.4113862354514848]
}
```

***

### **[GET]** /games

Summary  
- List of NFL Games

Description  
- Generate an array of all recorded games

#### Responses

- 200 Successful Response

`application/json`

```ts
[
	{
		_id: string // 075dbff0219a3a1100c513400c4796ef
		timestamp: string // 2022-11-04T00:15:00
		endTimestamp: string // "2022-11-04T03:05:00"
		home_team: string // Houston Texans
		home_score: number // 17
		away_team: string // 2022
		winner: string // "Philadelphia Eagles"
		duration: string // "2:50"
	}
]
```

***

### **[GET]** /most_positive/{data_source}

Summary  
- Get Most Positive Team

Description  
- Return the NFL team with highest positive sentiment  
  
- data_source: data source to use; reddit or twitter

#### Parameters(Path)
```ts
data_source: "reddit" | "twitter"
```

#### Responses

- 200 Successful Response

`application/json`

```ts
string // "baltimore-ravens"
```

***

### **[GET]** /least_postive/{data_source}

Summary  
- Get Least Positive Team

Description  
- Return the NFL team with lowest positive sentiment  
  
- data_source: Name of social media site

#### Parameters(Path)
```ts
data_source: "reddit" | "twitter"
```

#### Responses

- 200 Successful Response

`application/json`

```ts
string // "las-vegas-raiders"
```

***

### **[GET]** /positivity_sort/{data_source}

Summary  
- Get Positivity Sort

Description  
- Generate a dataframe of NFL teams sorted by positivity  
  
- data_source: data source to use; reddit or twitter

#### Parameters(Path)
```ts
data_source: "reddit" | "twitter"
```

#### Responses

- 200 Successful Response

`application/json`

```ts
[string, number][] // [["baltimore-ravens", 8.006139505827427], ..., ["las-vegas-raiders", 3.5768940857376483]] 
```

***

### **[GET]** /odds/odds_ts

Summary  
- Get Bookmaker Odds

Description  
- Generate a dataframe of all bookmaker odds for a specific game in timeseries formatting; use `/games` to fetch an applicable `game_id` 
  
- game_id: game id of desired game; can be provided by /games

#### Parameters(Query)

```ts
game_id: string // 38bf123ec9df3af4efff83e45f472c61
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
	string:	[{
	  time: string // "2022-11-18 16:59:09.263000"
	  team1_name: string // "Chicago Bears"
	  team1_odds: number // 152
	  team2_name: string // "New York Jets"
	  team2_odds: number // -180
	}]
}
```

***

### **[GET]** /odds/odds_avg

Summary  
- Get Average Bookmaker Odds

Description  
- Generate a dataframe of average bookmaker odds for a specific game  
  
- game_id: game id of desired game; can be provided by /games

#### Parameters(Query)

```ts
game_id: string // 38bf123ec9df3af4efff83e45f472c61
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
	[key: str]:	{
	  team1_name: string // "Chicago Bears"
	  team1_odds: number // 194.12056737588654
	  team2_name: string // "New York Jets"
	  team2_odds: number // -234.2127659574468
	}
}
```

***

### **[GET]** /graph/odds

Summary  
- Graph Betting Odds

Description  
- Generate graph of specified bookmaker odds for a desired game  
  
- game_id: game id of desired game; can be provided by /games
- bookmaker: bookmaker to use; fuzzy searchable (draft -> "DraftKings")
  
Dotted vertical line indicates winner

#### Parameters(Query)

```ts
game_id: string // 49b82cfa8d543643cf2b5d5109afa7be
```

```ts
bookmaker: string // fanduels
```

#### Responses

- 200 Successful Response

`image/png`

![image](https://user-images.githubusercontent.com/34300238/208235687-b49618eb-ed9a-43ce-8e85-deaaa8ee1edf.png)

> The vertical dotted line marks the start of the game, the color of the line matches the winner

> Notice that odds fluctuate greatly after the dotted line due to mid-game betting

***

### **[GET]** /graph/team/{team_name}

Summary  
- Graph Team Polarity

Description  
- Generate graph of polarity for specified team  
  
- team_name: name of the team; fuzzy search enabled ("buffalo" -> "Buffalo Bills")
- data_source:data source to use; reddit or twitter
- sample_window: a `timedelta` template string to be used for the moving average calculation
- resample_window: a `timedelta` template string to be used for the graphing interval (otherwise every point is shown which takes *forver* to render)

#### Parameters(Path)

```ts
team_name: TeamNameLiteral // Philidelphia Eagles
```

#### Parameters(Query)

```ts
data_source: "reddit" | "twitter" // reddit
```

```ts
sample_window?: string // 3D
```

```ts
resample_window?: string // 3H
```

#### Responses

- 200 Successful Response

`image/png`

![image](https://user-images.githubusercontent.com/34300238/208235697-294ae9ba-c1cc-45c9-922a-589c4011e34c.png)

>Vertical bars indicate the the start to end time of a game; the color of the bar indicates the outcome. 

>Green ✅= Win, Red ❌= Loss 

***

### **[GET]** /graph/game/{game_id}

Summary  
- Graph Team Vs Team Polarities

Description  
- Generate graph of team VS team polarities  

- game_id: game id of desired game; can be provided by /games
- data_source: data source to use; reddit or twitter

#### Parameters(Path)

```ts
game_id: string // 38bf123ec9df3af4efff83e45f472c61
```

#### Parameters(Query)

```ts
data_source: "reddit" | "twitter" // reddit
```

#### Responses

- 200 Successful Response

`image/png`

![image](https://user-images.githubusercontent.com/34300238/208235706-35c04905-4e6c-4e08-b20d-931aa75a2207.png)

> The vertical bar indicates the start and end of the game; the color of the bar matches the winning team.

> Notice how the losing team has a bigger sentiment drop; we attribute the drop in the winning team to general less activity

***

### **[GET]** /diff/{game_id}

Summary  
- Calculate Game Difference

Description  
- Calculate overall difference in sentiment between two teams  

- game_id: game id of desired game; can be provided by /games
- data_source: data source to use; reddit or twitter

#### Parameters(Path)

```ts
game_id: string // 38bf123ec9df3af4efff83e45f472c61
```

#### Parameters(Query)

```ts
data_source: "reddit" | "twitter" // reddit
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
	<team_name_1>: number
	<team_name_2>: number
	delta: number
	predicted_winner: <team_name_1> | <team_name_2>
	winner: <team_name_1> | <team_name_2>
	theory_supporting: bool
}
```

## References

### #/components/schemas/TeamNameLiteral

```ts
[
	"Philadelphia Eagles",
	"Buffalo Bills",
	"Green Bay Packers",
	"Minnesota Vikings",
	"Los Angeles Chargers",
	"Carolina Panthers",
	"Miami Dolphins",
	"Indianapolis Colts",
	"Las Vegas Raiders",
	"Seattle Seahawks",
	"Los Angeles Rams",
	"Tennessee Titans",
	"Baltimore Ravens",
	"Atlanta Falcons",
	"Cleveland Browns",
	"Denver Broncos",
	"Houston Texans",
	"Detroit Lions",
	"Jacksonville Jaguars",
	"New Orleans Saints",
	"Dallas Cowboys",
	"Arizona Cardinals",
	"Washington Commanders",
	"New York Jets",
	"Chicago Bears",
	"Cincinnati Bengals",
	"Kansas City Chiefs",
	"San Francisco 49ers",
	"New York Giants",
	"New England Patriots",
	"Tampa Bay Buccaneers",
	"Pittsburgh Steelers",
]
```
