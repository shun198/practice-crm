import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import router from 'next/router';

function ProductList() {
  // const [count, setCount] = useState(0);
  // const [count2, setCount2] = useState(0);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  // レンダリングのたびに実行
  // useEffect(() => {
  //   console.log('useEffectが実行されました');
  // });
  // // コンポーネントが表示される最初の1回だけ実行される
  // // コンポーネントの更新のたびに実行されるのを防ぐ
  // useEffect(() => {
  //   console.log('useEffect[]が実行されました');
  // }, []);
  // // countが変わる時だけStateを実行する
  // useEffect(() => {
  //   console.log('count2が増加しました');
  // }, [count2]);

  useEffect(() => {
    // データを取得するためのAPIのURLを指定
    const apiUrl = 'http://localhost/back/api/product/'; // 実際のAPIエンドポイントに置き換えてください
    const csrftoken = Cookies.get('csrftoken') || '';
    const credentials = 'include';

    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      credentials: credentials,
    })
    .then((response) => {
      if (response.ok) {
        // ステータスコードが200の場合、JSONデータを取得
        return response.json();
      } else if (response.status === 400) {
        // ステータスコードが400の場合、クライアントエラー
        throw new Error('クライアントエラー');
      } else if (response.status === 403) {
        // ステータスコードが403の場合、アクセス拒否
        router.push('/');
      } else if (response.status === 404) {
        router.push('/404');
      } else {
        // その他のステータスコードに対するエラーハンドリング
        throw new Error('その他エラー');
      }
    })
    .then((data) => {
      setData(data);
      setLoading(false);
    })
    .catch((error) => {
      console.error('データの取得に失敗しました:', error);
    });
}, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="App">
      {/* <h1>Learn useEffect</h1>
      <h2>Count: {count}</h2>
      <h2>Count2: {count2}</h2>
      <button onClick={() => setCount(count + 1)}>+</button>
      <br />
      <button onClick={() => setCount2(count2 + 1)}>+</button> */}
      <br />
      <div>
      <h1>商品一覧</h1>
      <table>
        <thead>
          <tr>
            <th>商品名</th>
            <th>商品の詳細</th>
            <th>商品の金額</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.details}</td>
              <td>{item.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </div>
  );
}

export default ProductList;