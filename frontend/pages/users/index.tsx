import React, {useState} from 'react';
import Link from "next/link";


const UserList = () => {
  const [products, setProducts] = useState([]);

  async function GetProductList() {
    try {
    const response = await fetch(
      'http://localhost/back/api/product/',
      {
        method: 'GET',
      }
    );

    if (response.status === 404) {
      throw new Error(
        '404 Not Found! Check if you are accessing the right url'
      );
    } else if (!response.ok) {
      throw new Error('Something went wrong!');
    }
    const data = await response.json();
    console.log('responseの中身');
    console.log(response);
    console.log('-------');
    console.log('dataの中身');
    console.log(data);
    console.log('-------');
    const productDataArray = data.map((productData) => {
      console.log('productDataArrayの中身');
      console.log(productData);
      console.log('-------');
      return {
        id: productData.id,
        name: productData.name,
        details: productData.details,
        price: productData.price,
        created_at: productData.created_at,
        updated_at: productData.updated_at
      };
    });
    setProducts(productDataArray)
    console.log(productDataArray)
    } catch (error) {
    }
  }

  return (
    <>
      <h1>システムユーザ一覧</h1>
      <h1>商品一覧</h1>
      <div>
      {products.map((ProductData) => (
          <ul key={ProductData.id}>
            <li>{ProductData.name}</li>
            <li>{ProductData.details}</li>
            <li>{ProductData.price}</li>
            <li>{ProductData.created_at}</li>
            <li>{ProductData.updated_at}</li>
          </ul>
        ))} 
      </div>
      <button onClick={GetProductList} >一覧を表示</button>
      <thead>
        <tr>
          <th>商品ID</th>
          <th>商品名</th>
          <th>商品の詳細</th>
          <th>商品の金額</th>
        </tr>
      </thead>
      <tbody>
        {products.length !== 0 && products.map((ProductData) => (
          <tr key={ProductData.id}>
            <td>{ProductData.name}</td>
            <td>{ProductData.details}</td>
            <td>{ProductData.price}</td>
          </tr>
        ))}
        {/* <tr key="1">
          <td>1</td>
          <td>ソファー</td>
          <td>ふかふか</td>
          <td>100000</td>
        </tr> */}
      </tbody>
      <div>
        <Link href="/"><h1>Homeへ</h1></Link>
      </div>
    </>
  );
};

export default UserList;