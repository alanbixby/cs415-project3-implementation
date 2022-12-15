import React from 'react'
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import styles from "../styles/Home.module.css"


const BarChart = ({ data }) => {
    // console.log(data[1]);
    return (
        <div className={styles.card}>
            <Bar
                datasetIdKey='id'
                data={{
                    labels: data[0],
                    datasets: [{
                        data: data[1],
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }],
                }}
            />
        </div>
    )
}


export default BarChart;