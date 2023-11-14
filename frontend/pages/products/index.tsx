import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import router from 'next/router';

function ProductList() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [loggedIn, setLoggedIn] = useState(true); // ログイン状態を管理

  useEffect(() => {
    // データを取得するためのAPIのURLを指定
    const apiUrl = "http://localhost/back/api/product/";
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
        console.log(response)
        console.log(loggedIn)
        setLoggedIn(true);
        console.log(loggedIn)
        return response.json();
      } else if (response.status === 403) {
        console.log(response)
        setLoggedIn(false); // ログインしていない状態をセット
      } else {
        console.log(response)
        console.log(process.env.NEXT_PUBLIC_BACK_)
        alert("エラーが発生しました")
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

  useEffect(() => {
    if (!loggedIn) {
    router.push('/'); // ログインしていない場合にルートページにリダイレクト
    }
  }, [loggedIn]);

  if (loading) {
    return <p>Loading...</p>;
  }


  return (
    <div className="App">
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
        {data && data.length > 0 ? (
            // data 配列が空でない場合のみマップ処理を行う
            data.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.details}</td>
                <td>{item.price}</td>
              </tr>
            ))
          ) : (
            // data 配列が空または未定義の場合の代替コンテンツ
            <tr>
              <td>Loading...</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
    </div>
  );
}

export default ProductList;