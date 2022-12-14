import mongoose from 'mongoose'
const { model, Schema } = mongoose

export interface IGamesSchema {
  _id: string
  timestamp: Date
  endTimestamp: Date
  duration: string
  home_team: string
  home_score: number
  away_team: string
  away_score: number
  winner: string
}

const GameSchema = new Schema<IGamesSchema>({
  _id: {
    type: String,
    alias: 'gameId',
  },
  timestamp: Date,
  endTimestamp: Date,
  duration: String,
  home_team: String,
  home_score: Number,
  away_team: String,
  away_score: Number,
  winner: String,
})

export const NFLGame: mongoose.Model<IGamesSchema> = model('games_schema', GameSchema, 'nfl_games')
