import { useForm } from "react-hook-form";
import Cookies from "js-cookie";
import router from "next/router";
import { Button, TextField } from "@mui/material";
import { ForgotPasswordButton } from "../buttons/ForgotPasswordButton";
import { LoginDataType } from "./type";

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginDataType>({
    // ログインボタンを押した時のみバリデーションを行う
    reValidateMode: "onSubmit",
  });

  const onSubmit = async (data: LoginDataType) => {
    const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/login`;
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
      // ログイン成功
      await router.push("/customers");
      // リダイレクトなど、ログイン後の処理を追加
    } else {
      // ログイン失敗
      response.json().then((data) => {
        const msg = data.msg;
        alert(msg);
      });
    }
  };

  return (
    <div className="Login">
      <h1 className="flex justify-center my-[10px] text-3xl text-gray-900">
        練習用アプリ
      </h1>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col items-center"
      >
        <TextField
          className="w-[400px] my-[10px]"
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
          <div className="text-red-500">{errors.employee_number.message}</div>
        )}
        <TextField
          className="w-[400px] my-[10px]"
          id="password"
          label="パスワード"
          placeholder="パスワード"
          type="password"
          {...register("password", {
            required: {
              value: true,
              message: "パスワードを入力してください",
            },
            // pattern: {
            //   value: /^(?=.*[a-zA-Z])(?=.*\d).{8,32}$/,
            //   message: '8文字以上、32文字以下の少なくとも1つ以上の半角英字と数字をもつパスワードを入力してください。',
            // },
          })}
        />
        {errors.password?.message && (
          <div className="text-red-500">{errors.password.message}</div>
        )}
        <Button
          type="submit"
          size="large"
          variant="contained"
          color="primary"
          className="w-[400px] my-[10px]"
        >
          ログイン
        </Button>
        <ForgotPasswordButton />
      </form>
    </div>
  );
}

export default LoginForm;
