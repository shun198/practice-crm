import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import router from "next/router";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import { BasicMenu } from "@/components/buttons/MenuButton";
import { Button } from "@mui/material";
import Pagination from "@mui/material/Pagination";
import CreateUserDialog from "@/components/dialogs/CreateUserDialog";

type CustomerData = {
  id: number;
  created_at: string;
  name: string;
  kana: string;
  updated_by: string;
};

type CustomerArray = CustomerData[];

function CustomerList() {
  const [data, setData] = useState<CustomerArray>([]);
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理

  const fetchData = async () => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/customers`;
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
        const responseData: CustomerArray = await response.json();
        setData(responseData);
        setLoggedIn(true);
      } else if (response.status === 401 || 403) {
        setLoggedIn(false);
      } else {
        alert("エラーが発生しました");
      }
    } catch (error) {
      console.error("データの取得に失敗しました:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (!loggedIn) {
      router.push("/");
    }
  }, [loggedIn]);

  if (!data || !data.results) return null;

  return (
    <div className="customer-list">
      <BasicMenu />
      <br />
      <div className="flex flex-col items-center my-[10px]">
        <h1 className="text-3xl text-gray-900">お客様情報一覧</h1>
      </div>
      <div className="flex flex-col items-end my-[10px]">
        <CreateUserDialog />
      </div>
      <div>
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
              {/* 他のセルのヘッダーも同様に追加 */}
              <TableCell align="center" className="font-bold">
                担当者
              </TableCell>
              <TableCell align="center" className="font-bold"></TableCell>
            </TableRow>
          </TableHead>
          {data.results.map((item, index) => {
            return (
              <TableBody key={index}>
                <TableCell align="center">{item.created_at}</TableCell>
                <TableCell align="center">{item.name}</TableCell>
                <TableCell align="center">{item.kana}</TableCell>
                {/* 他のセルも同様に追加 */}
                <TableCell align="center">{item.updated_by}</TableCell>
                <TableCell align="center">
                  <Button
                    size="small"
                    variant="contained"
                    className="w-[100px] my-[10px]"
                    onClick={() => router.push(`/customers/${item.id}`)}
                  >
                    詳細
                  </Button>
                </TableCell>
              </TableBody>
            );
          })}
        </Table>
      </div>
      <div>
        <Pagination
          count={data.final} //総ページ数
          color="primary" //ページネーションの色
          onChange={(e, page) => setPage(page)} //変更されたときに走る関数。第2引数にページ番号が入る
          page={data.current} //現在のページ番号
        />
      </div>
    </div>
  );
}

export default CustomerList;
