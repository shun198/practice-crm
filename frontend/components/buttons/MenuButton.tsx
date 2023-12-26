import { useState, MouseEvent } from "react";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Cookies from "js-cookie";
import router from "next/router";

export const BasicMenu = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const onSubmitCustomerList = () => {
    router.push("/customers");
  };

  const onSubmitUserList = () => {
    router.push("/users");
  };

  const onSubmitLogout = async () => {
    const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/logout`;
    const csrftoken = Cookies.get("csrftoken") || "";
    // ログイン情報をサーバーに送信
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    });

    if (response.ok) {
      // ログアウト成功
      router.push("/");
      // リダイレクトなど、ログイン後の処理を追加
    }
  };

  return (
    <div className="grid justify-items-end">
      <Button
        id="basic-button"
        aria-controls={open ? "basic-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleClick}
        variant="contained"
        color="inherit"
        size="large"
      >
        メニュー
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          "aria-labelledby": "basic-button",
        }}
      >
        <MenuItem onClick={onSubmitCustomerList}>お客様一覧へ</MenuItem>
        <MenuItem onClick={onSubmitUserList}>ユーザ一覧へ</MenuItem>
        <MenuItem onClick={onSubmitLogout}>ログアウト</MenuItem>
      </Menu>
    </div>
  );
};
