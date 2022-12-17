import { accessSync, existsSync } from 'fs';
import { readFile, writeFile } from 'fs/promises';

let data;
const __data = process.cwd() + '/fetch-cache.json';

const transpose = arr => arr[0].map((_, colIndex) => arr.map(row => row[colIndex]));

export default async function handler(req, res) {
    if (!data) {
        if (existsSync(__data)) {
            data = JSON.parse(await readFile(__data, 'utf8'));
        } else {
            data = await fetchData();
            await writeFile(__data, JSON.stringify(data));
        }
    }
    res.setHeader('Cache-Control', 's-ma`xage=86400');
    res.status(200).json(data);
}

async function fetchData() {
  const baseUrl = "http://localhost:5000";
  const apiEndpoints = [
    "/positivity_sort/twitter",
    "/positivity_sort/reddit",
    "/df/Houston%20Texans/reddit/sentiment",
    "/df/Houston%20Texans/reddit/frequency",
    "/df/Houston%20Texans/twitter/sentiment",
    "/df/Philadelphia%20Eagles/twitter/sentiment",
    "/df/Buffalo%20Bills/twitter/sentiment",
  ];

  const queryParams = "?focus_datetime=2022-11-14T12%3A00%3A00%2B00%3A00&window_before=172800&window_after=172800&sample_window=2D&resample_window=90T&all_data=false";

  const [
    res,
    res2,
    sentRes,
    freqRes,
    sentRes1,
    sentRes2,
    sentRes3,
  ] = await Promise.all(
    apiEndpoints.map((endpoint) => fetch(baseUrl + endpoint + queryParams))
  );

  const [
    sentData,
    freqData,
    sentData1,
    sentData2,
    sentData3,
  ] = await Promise.all([
    sentRes.json(),
    freqRes.json(),
    sentRes1.json(),
    sentRes2.json(),
    sentRes3.json(),
  ]);

  const [dataToCopy, dataToCopy2] = await Promise.all([res.json(), res2.json()]);

  dataToCopy.sort((a, b) => (a[0] == b[0] ? 0 : a[0] < b[0] ? -1 : 1));
  dataToCopy2.sort((a, b) => (a[0] == b[0] ? 0 : a[0] < b[0] ? -1 : 1));

  const dataToCopyNew = transpose(dataToCopy);
  const dataToCopyNew2 = transpose(dataToCopy2);

  const data = {
    sentiment_data: sentData,
    twitterData: dataToCopyNew,
    redditData: dataToCopyNew2,
    new_sentiment_data: [sentData1, sentData2, sentData3],
    frequency_data: freqData,
  };

  // return
  return data
}