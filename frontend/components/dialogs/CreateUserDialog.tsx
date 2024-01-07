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
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { CreateUserType } from "../forms/type";

function CreateUserDialog() {
  const [loggedIn, setLoggedIn] = useState<Boolean>(true); // ログイン状態を管理

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateUserType>({
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

  const onSubmit = async (data: CreateUserType) => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/customers`;
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
            console.log(data[key]);
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
        お客様登録
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col items-center"
        >
          <DialogTitle>お客様の登録</DialogTitle>
          <DialogContent>
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="name"
              label="氏名"
              placeholder="氏名"
              type="text"
              {...register("customer.name", {
                required: {
                  value: true,
                  message: "氏名を入力してください",
                },
              })}
            />
            {errors.customer?.name?.message && (
              <div className="text-red-500">
                {errors.customer?.name?.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="kana"
              label="カナ氏名"
              placeholder="カナ氏名"
              type="text"
              {...register("customer.kana", {
                required: {
                  value: true,
                  message: "カナ氏名を入力してください",
                },
              })}
            />
            {errors.customer?.kana?.message && (
              <div className="text-red-500">
                {errors.customer?.kana?.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="email"
              label="メールアドレス"
              placeholder="メールアドレス"
              type="email"
              {...register("customer.email", {
                required: {
                  value: true,
                  message: "メールアドレスを入力してください",
                },
              })}
            />
            {errors.customer?.email?.message && (
              <div className="text-red-500">
                {errors.customer?.email.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="phone_no"
              label="電話番号"
              placeholder="電話番号"
              type="text"
              {...register("customer.phone_no", {
                required: {
                  value: true,
                  message: "電話番号を入力してください",
                },
                pattern: {
                  value: /^[0-9]{10,11}$/,
                  message: "10桁または11桁の数字のみ入力してください",
                },
              })}
            />
            {errors.customer?.phone_no?.message && (
              <div className="text-red-500">
                {errors.customer?.phone_no.message}
              </div>
            )}
            {/* <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DatePicker']}>
                <DatePicker label="Basic date picker" />
            </DemoContainer>
            </LocalizationProvider> */}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="prefecture"
              label="都道府県"
              placeholder="都道府県"
              type="text"
              {...register("address.prefecture", {
                required: {
                  value: true,
                  message: "都道府県を入力してください",
                },
              })}
            />
            {errors.address?.prefecture?.message && (
              <div className="text-red-500">
                {errors.address?.prefecture?.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="municipalities"
              label="市区町村"
              placeholder="市区町村"
              type="text"
              {...register("address.municipalities", {
                required: {
                  value: true,
                  message: "市区町村を入力してください",
                },
              })}
            />
            {errors.address?.municipalities?.message && (
              <div className="text-red-500">
                {errors.address?.municipalities?.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="house_no"
              label="丁・番地"
              placeholder="丁・番地"
              type="text"
              {...register("address.house_no", {
                required: {
                  value: true,
                  message: "丁・番地を入力してください",
                },
              })}
            />
            {errors.address?.house_no?.message && (
              <div className="text-red-500">
                {errors.address?.house_no?.message}
              </div>
            )}
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="other"
              label="その他(マンション名など)"
              placeholder="その他(マンション名など)"
              type="text"
              {...register("address.other", {
                required: false,
              })}
            />
            <TextField
              className="w-[400px] my-[10px]"
              autoFocus
              id="post_no"
              label="郵便番号"
              placeholder="郵便番号"
              type="text"
              {...register("address.post_no", {
                required: {
                  value: true,
                  message: "郵便番号を入力してください",
                },
                pattern: {
                  value: /^[0-9]{7}$/,
                  message: "7桁の数字のみ入力してください",
                },
              })}
            />
            {errors.address?.post_no?.message && (
              <div className="text-red-500">
                {errors.address?.post_no?.message}
              </div>
            )}
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

export default CreateUserDialog;
