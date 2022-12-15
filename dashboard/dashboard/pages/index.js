import styles from "../styles/Home.module.css"
import { useRouter } from 'next/router'
import DoughnutChart from "../components/LineChart"
import ChartGrid from "../components/ChartGrid"
// import map

const transpose = arr => arr[0].map((_, colIndex) => arr.map(row => row[colIndex]));

export default function Home({ data }) {
  console.log(data[0])
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
  console.log(dataToCopy)
  const dataToCopyNew = transpose(dataToCopy)
  const dataToCopyNew2 = transpose(dataToCopy2)
  const data = {
    twitterData: dataToCopyNew,
    redditData: dataToCopyNew2
  }
  return {
    props: {
      data
    }
  }
}