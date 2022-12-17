import ChartGrid from "../components/ChartGrid";
import styles from "../styles/Home.module.css";
// import map

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
  const data = await (await fetch('http://localhost:3000/api/fetchData')).json();
  return { props: { data } }
}