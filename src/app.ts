import chalk from 'chalk'
import cheerio from 'cheerio'
import 'dotenv/config'
import { gotScraping as got } from 'got-scraping'
import { NFLGame } from './schemas/gamesSchema.js'
import { DraftKingGame } from './schemas/oddsSchema.js'
import mongo from './util/mongo.js'

await mongo(process.env.MONGO_URI as string, 'cs415_production')

const domain = 'https://www.pro-football-reference.com/years/2022/games.htm'
const html = await got.get(domain, { resolveBodyOnly: true })
// console.log(html)
const $ = cheerio.load(html)
const links = $("table td[data-stat='boxscore_word'] a")
  .map(function () {
    return $(this).attr('href')
  })
  .get()

console.log(links)

// Running this assumes NFLGames is already initialized from Project-2-Implementaton
for (const link of links) {
  // Use this to skip games that have already been scraped if ratelimiting occurs
  // if (matchList.includes(`https://www.pro-football-reference.com${link}`) || !link.includes('202211')) {
  //   continue
  // }
  const html = await got.get(`https://www.pro-football-reference.com${link}`, { resolveBodyOnly: true })
  // console.log(html)
  const $ = cheerio.load(html)
  const duration = $('div strong:contains("Time of Game")').parent().text().substring(14)
  const [hours, minutes] = duration.split(':')
  const homeTeam = $(
    '.scorebox > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2) > a:nth-child(1)'
  ).text()
  const awayTeam = $(
    '.scorebox > div:nth-child(2) > div:nth-child(1) > strong:nth-child(2) > a:nth-child(1)'
  ).text()
  const startDate = new Date($('.scorebox_meta > div:nth-child(1)').text())
  console.log(startDate)
  console.log(`${homeTeam} vs ${awayTeam}`)
  console.log(hours, minutes)
  console.log(`https://www.pro-football-reference.com${link}`)

  const gameId = await DraftKingGame.findOne({
    home_team: homeTeam,
    away_team: awayTeam,
  })

  await new Promise((resolve) => setTimeout(resolve, 1000))
  if (!gameId) {
    console.log(chalk.red("Couldn't find game"))
    continue
  }

  const nflGame = await NFLGame.findOne({ _id: gameId._id })
  if (!nflGame) {
    console.log(chalk.red("Couldn't find game"))
    continue
  }

  const output = await NFLGame.findOneAndUpdate(
    { _id: gameId._id },
    {
      $set: {
        endTimestamp: new Date(
          nflGame?.timestamp?.getTime() + parseInt(hours) * 60 * 60 * 1000 + parseInt(minutes) * 60 * 1000
        ),
        duration: duration,
      },
    },
    {
      new: true,
    }
  )
  console.log(output)
  // break
}

console.log('done')
