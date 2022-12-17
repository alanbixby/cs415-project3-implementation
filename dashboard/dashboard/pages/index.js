import styles from "../styles/Home.module.css"
import { useRouter } from 'next/router'
import DoughnutChart from "../components/LineChart"
import ChartGrid from "../components/ChartGrid"
// import map

const transpose = arr => arr[0].map((_, colIndex) => arr.map(row => row[colIndex]));

export default function Home({ data }) {
  console.log(data.frequency_data)
  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Gatorade Dashboards</h3>
      <ChartGrid data={data}/>
    </div>
  )
}

// If you export a function called getServerSideProps (Server-Side Rendering) 
// from a page, Next.js will pre-render this page on each request using the 
// data returned by getServerSideProps.
export const getServerSideProps = async () => {
  const res = await fetch("http://localhost:5000/positivity_sort/twitter")
  const res2 = await fetch("http://localhost:5000/positivity_sort/reddit")
  const sent_res = await fetch("http://localhost:5000/df/Houston%20Texans/reddit/sentiment?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false")

  const freq = await fetch("http://localhost:5000/df/Houston%20Texans/reddit/frequency?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false")

  const sent_res1 = await fetch("http://localhost:5000/df/Houston%20Texans/twitter/sentiment?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false")
  const sent_res2 = await fetch("http://localhost:5000/df/Philadelphia%20Eagles/twitter/sentiment?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false")
  const sent_res3 = await fetch("http://localhost:5000/df/Buffalo%20Bills/twitter/sentiment?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false")

  const sent_data1 = await sent_res1.json()
  const sent_data2 = await sent_res2.json()
  const sent_data3 = await sent_res3.json()

  const freq_data = await freq.json()


  const sent_data = await sent_res.json()
  const dataToCopy = await res.json()
  const dataToCopy2 = await res2.json()
  //
  dataToCopy.sort( function( a, b )
  {
    // Sort by the 2nd value in each array
    if ( a[0] == b[0] ) return 0;
    return a[0] < b[0] ? -1 : 1;
  })
  dataToCopy2.sort( function( a, b )
  {
    // Sort by the 2nd value in each array
    if ( a[0] == b[0] ) return 0;
    return a[0] < b[0] ? -1 : 1;
  })
  // console.log(dataToCopy)
  const dataToCopyNew = transpose(dataToCopy)
  const dataToCopyNew2 = transpose(dataToCopy2)
  // const new_sent_data = transpose(sent_data)
  // console.log(sent_data)
  const data = {
    sentiment_data: sent_data,
    twitterData: dataToCopyNew,
    redditData: dataToCopyNew2,
    new_sentiment_data: [sent_data1, sent_data2, sent_data3],
    frequency_data: freq_data
  }
  return {
    props: {
      data
    }
  }
}