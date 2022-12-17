import React from 'react'
import { Line } from 'react-chartjs-2';
import styles from "../styles/Home.module.css"


const LineChart = ({ data: input }) => {
    // console.log(input[0][0])
    return (
        <div className={styles.card}>
            <Line
                datasetIdKey='id'
                data={{
                        labels: input[0][0],
                        datasets: [{
                            id: 1,
                            label: 'twitter positivity',
                            data: input[0][1],
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        },{
                            id: 2,
                            label: 'reddit positivity',
                            data: input[1][1],
                            fill: false,
                            borderColor: 'rgb(75, 200, 120)',
                            tension: 0.1
                        }],
                }}
            />
        </div>
    )
}


export default LineChart;