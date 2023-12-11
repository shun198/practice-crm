import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";

type CustomerDetailData = {
  id: number;
  name: string;
  kana: string;
  birthday: Date;
  email: string;
  phone_no: string;
  address: string;
  post_no: string;
  updated_by: string;
};

function CustomerDetail() {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState<Boolean>(true);
  const [data, setData] = useState<any>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = `http://localhost/back/api/customers/${router.query.id}/`;
        const csrftoken = Cookies.get("csrftoken") || "";
        const credentials = "include";
        const response = await fetch(apiUrl, {
          method: "GET",
          headers: {
            "X-CSRFToken": csrftoken,
          },
          credentials: credentials,
        });

        if (response.ok) {
          const responseData: CustomerDetailData = await response.json();
          setData(responseData);
          setLoggedIn(true);
        } else if (response.status === 403) {
          setLoggedIn(false);
          router.push("/"); // ログインしていない場合にルートページにリダイレクト
        } else {
          alert("エラーが発生しました");
        }
      } catch (error) {
        console.error("データの取得に失敗しました:", error);
      }
    };

    if (router.isReady) {
      fetchData();
    }
  }, [router]);

  useEffect(() => {
    if (!loggedIn) {
      router.push("/");
    }
  }, [loggedIn]);

  if (!data) return null;

  return (
    <div className="customer-details">
      <h1>お客様詳細</h1>
      <div>{data.name}</div>
      <div>{data.kana}</div>
      <div>{data.birthday}</div>
      <div>{data.email}</div>
      <div>{data.phone_no}</div>
      <div>{data.address}</div>
      <div>{data.post_no}</div>
      {/* 担当者 */}
      <div>{data.updated_by}</div>
    </div>
  );
}

export default CustomerDetail;
