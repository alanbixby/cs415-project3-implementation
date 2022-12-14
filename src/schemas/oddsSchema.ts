import mongoose from 'mongoose'
const { model, Schema } = mongoose

export interface IOddsSchema {
  _id: string
  sports_key: string
  sport_title: string
  home_team: string
  away_team: string
  commence_time: Date
  last_update: string
}

const OddsSchema = new Schema<IOddsSchema>({
  _id: {
    type: String,
  },
  sports_key: String,
  sport_title: String,
  home_team: String,
  away_team: String,
  commence_time: Date,
  last_update: String,
})

export const DraftKingGame: mongoose.Model<IOddsSchema> = model('odds_schema', OddsSchema, 'odds_draftkings')
export const FanDuelGame: mongoose.Model<IOddsSchema> = model('odds_schema', OddsSchema, 'odds_fanduel')
export const BarstoolGame: mongoose.Model<IOddsSchema> = model('odds_schema', OddsSchema, 'odds_barstool')
