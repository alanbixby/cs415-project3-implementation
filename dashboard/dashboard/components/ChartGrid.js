import React from 'react'
import styles from "../styles/Home.module.css"
import BarChart from './BarChart'
import LineChart from './LineChart'
import ShoppingHourGraph from './shoppingHourGraph'
import ProductLineBySales from './ProductLineBySales'
import ProductLineByRating from './ProductLineByRating'
import PaymentMethod from './PaymentMethod'
import ProductLineByGrossIncome from './ProductLineByGrossIncome'
import ProductLineCombined from './ProductLineCombined'

const ChartGrid = ({ data }) => {
    return (
        <div className={styles.grid}>
            <LineChart data={[data.twitterData,data.redditData]} />
            <BarChart data={data.redditData} />
            {/*<LineChart data={data.lineData2} />*/}

            {/* <ShoppingHourGraph data={data.data.shooping_hour_data} />
            <ProductLineBySales data={data.data.product_line_by_total_sales} />
            <ProductLineByRating data={data.data.product_line_by_rating} />
            <ProductLineByGrossIncome data={data.data.product_line_by_gross_income} />
            <ProductLineCombined data1={data.data.product_line_by_total_sales}
                data2={data.data.product_line_by_rating}
                data3={data.data.product_line_by_gross_income} />
            <PaymentMethod data={data.data.payment_methods} />
            <SalesByGender data={data.data.sales_by_gender} /> */}
        </div>
    )
}

export default ChartGrid;