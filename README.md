# NFL Sentiment Analysis

> Version 0.1.0

An API for generating graphs and dataframes of sentiment analysis data for NFL teams on Reddit and Twitter 🏈

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/df/{team_name}/{collection}/{mode}](#getdfteam_namecollectionmode) | Generate Dataframe Data |
| GET | [/games](#getgames) | List Nfl Games |
| GET | [/most_positive/{data_source}](#getmost_positivedata_source) | Get Most Positive Team |
| GET | [/least_postive/{data_source}](#getleast_postivedata_source) | Get Least Positive Team |
| GET | [/positivity_sort/{data_source}](#getpositivity_sortdata_source) | Get Positivity Sort |
| GET | [/odds/odds_ts](#getoddsodds_ts) | Get Bookmaker Odds |
| GET | [/odds/odds_avg](#getoddsodds_avg) | Get Average Bookmaker Odds |
| GET | [/graph/odds](#getgraphodds) | Graph Betting Odds |
| GET | [/graph/team/{team_name}](#getgraphteamteam_name) | Graph Team Polarity |
| GET | [/graph/game/{game_id}](#getgraphgamegame_id) | Graph Team Vs Team Polarities |
| GET | [/diff/{game_id}](#getdiffgame_id) | Calculate Game Difference |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |

## Path Details

***

### [GET]/df/{team_name}/{collection}/{mode}

- Summary  
Generate Dataframe Data

- Description  
Generate a dataframe of data for a given team, data source, and metric; allows for custom time windows  
  
- team_name: Name of the team  
- collection: Data source to use  
- mode: Metric to use  
- focus_datetime: Datetime to center the window on  
- window_before: Time window before the focus datetime  
- window_after: Time window after the focus datetime  
- sample_window: Time window to sample the data at

#### Parameters(Query)

```ts
focus_datetime?: string
```

```ts
window_before?: number
```

```ts
window_after?: number
```

```ts
sample_window?: string
```

```ts
resample_window?: string
```

```ts
all_data?: boolean
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/games

- Summary  
List Nfl Games

- Description  
Generate a dataframe of all recorded games

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/most_positive/{data_source}

- Summary  
Get Most Positive Team

- Description  
Return the NFL team with highest positive sentiment  
  
- data_source: Name of social media site

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/least_postive/{data_source}

- Summary  
Get Least Positive Team

- Description  
Return the NFL team with lowest positive sentiment  
  
- data_source: Name of social media site

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/positivity_sort/{data_source}

- Summary  
Get Positivity Sort

- Description  
Generate a dataframe of NFL teams sorted by positivity  
  
- data_source: Name of social media site

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/odds/odds_ts

- Summary  
Get Bookmaker Odds

- Description  
Generate a dataframe of bookmaker odds for a specific game  
  
- game_id: ID of desired game

#### Parameters(Query)

```ts
game_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/odds/odds_avg

- Summary  
Get Average Bookmaker Odds

- Description  
Generate a dataframe of average bookmaker odds for a specific game  
  
- game_id: ID of desired game

#### Parameters(Query)

```ts
game_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/graph/odds

- Summary  
Graph Betting Odds

- Description  
Generate graph of specified bookmaker odds for a desired game  
  
- game_id: ID of desired game  
- bookmaker: Name of bookmaker  
  
Dotted vertical line indicates winner

#### Parameters(Query)

```ts
game_id: string
```

```ts
bookmaker: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/graph/team/{team_name}

- Summary  
Graph Team Polarity

- Description  
Generate graph of polarity for specified team  
  
- team_name: Name of desired team  
- data_source: Name of social media site  
- sample_window: Desired number of days in window  
- resample_window: Hourly resample rate within window

#### Parameters(Query)

```ts
data_source: string
```

```ts
sample_window?: string
```

```ts
resample_window?: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/graph/game/{game_id}

- Summary  
Graph Team Vs Team Polarities

- Description  
Generate graph of team VS team polarities  
- game_id: ID of desired game  
- data_source: Name of social media site or both

#### Parameters(Query)

```ts
data_source: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/diff/{game_id}

- Summary  
Calculate Game Difference

- Description  
Calculate overall difference in sentiment between two teams  
- game_id: ID of desired game  
- data_source: Name of social media site

#### Parameters(Query)

```ts
data_source: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
