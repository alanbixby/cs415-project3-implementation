import React from 'react'
import { Line } from 'react-chartjs-2';
import styles from "../styles/Home.module.css"


const LineChart3 = ({ data: input }) => {
    // console.log(input[0][0])
    return (
        <div className={styles.card}>
            <Line
                datasetIdKey='id'
                data={{
                        datasets: [{
                            id: 1,
                            label: 'Houston Texans twitter polarity',
                            data: input[0].polarity,
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        },{
                            id: 2,
                            label: 'Philadelphia Eagles twitter polarity',
                            data: input[1].polarity,
                            fill: false,
                            borderColor: 'rgb(75, 200, 120)',
                            tension: 0.1
                        },{
                            id: 3,
                            label: 'Buffalo Bills twitter polarity',
                            data: input[2].polarity,
                            fill: false,
                            borderColor: 'rgb(75, 120, 200)',
                            tension: 0.1
                        }],
                }}
            />
        </div>
    )
}


export default LineChart3;