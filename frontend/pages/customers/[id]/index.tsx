import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { TextField } from "@mui/material";

function CustomerDetail() {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState<Boolean>(true);
  const [data, setData] = useState([]);
  const [id, setId] = useState<number>();

  useEffect(() => {
    // idがqueryで利用可能になったら処理される
    if (router.asPath !== router.route) {
      setId(Number(router.query.id));
    }
  }, [router]);

  useEffect(() => {
    const apiUrl = `http://localhost/back/api/customers/${router.query.id}/`;
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
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        console.error("データの取得に失敗しました:", error);
      });
  }, [router.query.id]);

  useEffect(() => {
    if (!loggedIn) {
      router.push("/"); // ログインしていない場合にルートページにリダイレクト
    }
  }, [loggedIn]);

  if (!data || !data.results) return null;
  return <TextField>aaa</TextField>;
}

export default CustomerDetail;
