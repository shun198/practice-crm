import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import router from 'next/router';

function ProductList() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

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