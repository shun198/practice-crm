import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import router from "next/router";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { Radio, RadioGroup, FormControlLabel } from "@mui/material";
import { InviteUserType } from "../forms/type";

function InviteUserDialog() {
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理
  const [value, setValue] = useState("0");
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<InviteUserType>({
    // ログインボタンを押した時のみバリデーションを行う
    reValidateMode: "onSubmit",
  });

  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const onSubmit = async (data: InviteUserType) => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/users/invite_user`;
      const credentials = "include";
      const csrftoken = Cookies.get("csrftoken") || "";
      // ログイン情報をサーバーに送信
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        // ユーザー名（社員番号）とパスワードをJSON形式で送信
        body: JSON.stringify(data),
        credentials,
      });

      if (response.ok) {
        setLoggedIn(true);
        response.json().then((data) => {
          const msg = data.msg;
          alert(msg);
          window.location.reload();
        });
      } else if (response.status === 401 || 403) {
        setLoggedIn(false);
      } else if (response.status === 400) {
        setLoggedIn(true);
        response.json().then((data) => {
          console.log(data);
          for (const key in data) {
            alert(data[key]);
          }
          handleClose();
        });
      } else {
        alert("エラーが発生しました");
      }
    } catch (error) {
      console.error("データの取得に失敗しました:", error);
    }
  };

  useEffect(() => {
    if (!loggedIn) {
      router.push("/");
    }
  }, [loggedIn]);

  return (
    <div>
      <Button
        type="submit"
        size="medium"
        variant="contained"
        color="primary"
        className="grid justify-items-end w-[200px] my-[20px]"
        onClick={handleClickOpen}
      >
        ユーザ招待
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col items-center"
        >
          <DialogTitle>システムユーザの登録</DialogTitle>
          <DialogContent>
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="employee_number"
              label="社員番号"
              placeholder="社員番号"
              type="text"
              {...register("employee_number", {
                required: {
                  value: true,
                  message: "社員番号を入力してください",
                },
                pattern: {
                  value: /^[0-9]{8}$/,
                  message: "8桁の数字のみ入力してください",
                },
              })}
            />
            {errors.employee_number?.message && (
              <div className="text-red-500">
                {errors.employee_number.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="username"
              label="システムユーザ名"
              placeholder="システムユーザ名"
              type="text"
              {...register("username", {
                required: {
                  value: true,
                  message: "システムユーザ名を入力してください",
                },
              })}
            />
            {errors.username?.message && (
              <div className="text-red-500">{errors.username.message}</div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="email"
              label="メールアドレス"
              placeholder="メールアドレス"
              type="email"
              {...register("email", {
                required: {
                  value: true,
                  message: "メールアドレスを入力してください",
                },
              })}
            />
            {errors.email?.message && (
              <div className="text-red-500">{errors.email.message}</div>
            )}
            <RadioGroup
              id="role"
              name="role"
              value={value}
              defaultValue="0"
              onChange={handleChange}
            >
              <FormControlLabel
                value="0"
                control={<Radio {...register("role", { value: "0" })} />}
                label="管理者"
              />
              <FormControlLabel
                value="1"
                control={<Radio {...register("role", { value: "1" })} />}
                label="一般"
              />
            </RadioGroup>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>閉じる</Button>
            <Button type="submit">登録</Button>
          </DialogActions>
        </form>
      </Dialog>
    </div>
  );
}

export default InviteUserDialog;
