import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import router from "next/router";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import { BasicMenu } from "@/components/buttons/MenuButton";

type ProductData = {
  name: string;
  details: string;
  price: number;
};

type ProductArray = ProductData[];

function ProductList() {
  const [data, setData] = useState<ProductArray>([]);
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理

  useEffect(() => {
    // データを取得するためのAPIのURLを指定
    const apiUrl = "http://localhost/back/api/customers/";
    const csrftoken = Cookies.get("csrftoken") || "";
    const credentials = "include";

    fetch(apiUrl, {
      method: "GET",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      credentials: credentials,
    })
      .then((response) => {
        if (response.ok) {
          // ステータスコードが200の場合、JSONデータを取得
          setLoggedIn(true);
          return response.json();
        } else if (response.status === 403) {
          setLoggedIn(false); // ログインしていない状態をセット
        } else {
          alert("エラーが発生しました");
        }
      })
      .then((data: ProductArray) => {
        setData(data);
      })
      .catch((error) => {
        console.error("データの取得に失敗しました:", error);
      });
  }, []);

  useEffect(() => {
    if (!loggedIn) {
      router.push("/"); // ログインしていない場合にルートページにリダイレクト
    }
  }, [loggedIn]);

  if (!data || !data.results) return null;

  return (
    <div className="product-list">
      <BasicMenu />
      <br />
      <div>
        <h1 className="flex flex-col items-center my-[10px] text-3xl text-gray-900">
          お客様情報一覧
        </h1>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="center" className="font-bold">
                受付日
              </TableCell>
              <TableCell align="center" className="font-bold">
                お客様氏名
              </TableCell>
              <TableCell align="center" className="font-bold">
                お客様カナ氏名
              </TableCell>
              <TableCell align="center" className="font-bold">
                メールアドレス
              </TableCell>
              <TableCell align="center" className="font-bold">
                電話番号
              </TableCell>
              <TableCell align="center" className="font-bold">
                担当者
              </TableCell>
            </TableRow>
          </TableHead>
          {data.results.map((item, index) => {
            return (
              <TableBody key={index}>
                <TableCell align="center">{item.created_at}</TableCell>
                <TableCell align="center">{item.name}</TableCell>
                <TableCell align="center">{item.kana}</TableCell>
                <TableCell align="center">{item.email}</TableCell>
                <TableCell align="center">{item.phone_no}</TableCell>
                <TableCell align="center">{item.updated_by}</TableCell>
              </TableBody>
            );
          })}
        </Table>
      </div>
    </div>
  );
}

export default ProductList;
