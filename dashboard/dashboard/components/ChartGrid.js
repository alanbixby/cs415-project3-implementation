import React from 'react'
import styles from "../styles/Home.module.css"
import BarChart from './BarChart'
import LineChart from './LineChart'
import LineChart2 from './LineChart2'
import LineChart3 from './LineChart3'

const ChartGrid = ({ data }) => {
    return (
        <div className={styles.grid}>
            <LineChart data={[data.twitterData,data.redditData]} />
            <BarChart data={data.frequency_data} />
            <LineChart2 data ={data.sentiment_data} />
            <LineChart3 data={data.new_sentiment_data} />

        </div>
    )
}

export default ChartGrid;