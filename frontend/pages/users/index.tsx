import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import router from "next/router";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import { BasicMenu } from "@/components/buttons/MenuButton";
import { Switch, Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

type UserData = {
  name: string;
  details: string;
  price: number;
};

type UserArray = UserData[];

function UserList() {
  const [data, setData] = useState<UserArray>([]);
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理
  const [checked, setChecked] = useState<Boolean>(false);

  useEffect(() => {
    // データを取得するためのAPIのURLを指定
    const apiUrl = "http://localhost/back/api/users/";
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
      .then((data: UserArray) => {
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
    <div className="customer-list">
      <BasicMenu />
      <br />
      <div>
        <h1 className="flex flex-col items-center my-[10px] text-3xl text-gray-900">
          システムユーザ一覧
        </h1>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="center" className="font-bold">
                社員番号
              </TableCell>
              <TableCell align="center" className="font-bold">
                システムユーザ名
              </TableCell>
              <TableCell align="center" className="font-bold">
                メールアドレス
              </TableCell>
              <TableCell align="center" className="font-bold">
                権限
              </TableCell>
              <TableCell align="center" className="font-bold">
                有効/無効
              </TableCell>
              <TableCell align="center" className="font-bold">
                再送信
              </TableCell>
              <TableCell align="center" className="font-bold"></TableCell>
            </TableRow>
          </TableHead>
          {data.results.map((item, index) => {
            return (
              <TableBody key={index}>
                <TableCell align="center">{item.employee_number}</TableCell>
                <TableCell align="center">{item.username}</TableCell>
                <TableCell align="center">{item.email}</TableCell>
                <TableCell align="center">{item.role}</TableCell>
                <TableCell align="center">
                  <Switch checked={item.is_active} />
                </TableCell>
                <TableCell align="center">
                  <Button
                    disabled={!item.is_active || item.is_verified}
                    size="small"
                    variant="contained"
                    color="success"
                    className="w-[100px] my-[10px]"
                  >
                    再送信
                    <SendIcon />
                  </Button>
                </TableCell>
                <TableCell align="center">
                  <Button
                    size="small"
                    variant="contained"
                    className="w-[100px] my-[10px]"
                  >
                    編集
                  </Button>
                </TableCell>
              </TableBody>
            );
          })}
        </Table>
      </div>
    </div>
  );
}

export default UserList;
