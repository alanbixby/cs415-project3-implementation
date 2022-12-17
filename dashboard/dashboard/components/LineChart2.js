import React from 'react'
import { Line } from 'react-chartjs-2';
import styles from "../styles/Home.module.css"


const LineChart2 = ({ data: input }) => {
    // console.log(input[0][0])
    return (
        <div className={styles.card}>
            <Line
                datasetIdKey='id'
                data={{
                        datasets: [{
                            id: 1,
                            label: 'reddit polarity for Houston Texans',
                            data: input.polarity,
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        },{
                            id: 2,
                            label: 'reddit subjectivity for Houston Texans',
                            data: input.subjectivity,
                            fill: false,
                            borderColor: 'rgb(75, 200, 120)',
                            tension: 0.1
                        }],
                }}
            />
        </div>
    )
}


export default LineChart2;