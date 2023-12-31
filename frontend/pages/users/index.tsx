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
import InviteUserDialog from "@/components/dialogs/InviteUserDialog";

type UserData = {
  id: number;
  employee_number: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
};

type UserArray = UserData[];

function UserList() {
  const [data, setData] = useState<UserArray>([]);
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理

  const fetchActive = async (id: string) => {
    try {
      // fetchAPIの処理を記載する
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/users/${id}/toggle_user_active`;
      const csrftoken = Cookies.get("csrftoken") || "";
      const credentials = "include";

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": csrftoken,
          "Cache-Control": "private",
        },
        credentials: credentials,
      });
      if (response.ok) {
        setLoggedIn(true);
        fetchUserData();
      } else if (response.status === 401 || 403) {
        setLoggedIn(false);
        router.push("/"); // ログインしていない場合にルートページにリダイレクト
      } else if (response.status === 404) {
        router.replace("/404"); // IDが存在しない場合は404ページへリダイレクト
      } else if (response.status === 400) {
        response.json().then((data) => {
          const msg = data.msg;
          alert(msg);
        });
      } else {
        alert("エラーが発生しました");
      }
    } catch (error) {
      if (error instanceof Error) {
        alert({ message: `${error.message}`, severity: "error" });
      }
    }
  };

  const switchHandler = (switchData: { id: String }) => {
    fetchActive(switchData.id);
  };

  const fetchUserData = async () => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/users`;
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
        const responseData: UserArray = await response.json();
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

  const reinviteUserHandler = async (id: String) => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/users/${id}/reinvite_user`;
      const csrftoken = Cookies.get("csrftoken") || "";
      const credentials = "include";

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        credentials: credentials,
      });

      if (response.ok) {
        setLoggedIn(true);
        response.json().then((data) => {
          const msg = data.msg;
          alert(msg);
        });
      } else if (response.status === 401 || 403) {
        setLoggedIn(false);
      } else if (response.status === 400) {
        setLoggedIn(true);
        response.json().then((data) => {
          const msg = data.msg;
          alert(msg);
        });
      } else {
        alert("エラーが発生しました");
      }
    } catch (error) {
      console.error("データの取得に失敗しました:", error);
    }
  };

  useEffect(() => {
    fetchUserData();
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
      <div>
        <h1 className="flex flex-col items-center my-[10px] text-3xl text-gray-900">
          システムユーザ一覧
        </h1>
        <div className="flex flex-col items-end my-[10px]">
          <InviteUserDialog />
        </div>
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
          {data.results.map((item, index) => (
            <TableBody key={index}>
              <TableCell align="center">{item.employee_number}</TableCell>
              <TableCell align="center">{item.username}</TableCell>
              <TableCell align="center">{item.email}</TableCell>
              <TableCell align="center">{item.role}</TableCell>
              <TableCell align="center">
                <Switch
                  checked={item.is_active}
                  onChange={() => switchHandler({ id: item.id })}
                />
              </TableCell>
              <TableCell align="center">
                <Button
                  disabled={item.is_verified}
                  size="small"
                  variant="contained"
                  color="success"
                  className="w-[100px] my-[10px]"
                  onClick={() => reinviteUserHandler(item.id)}
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
          ))}
        </Table>
      </div>
    </div>
  );
}

export default UserList;
