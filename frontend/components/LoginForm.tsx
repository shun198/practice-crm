import { useForm } from "react-hook-form";
import Cookies from "js-cookie";
import router from "next/router";
import { Button } from "@mui/material";
import { TextField } from "@mui/material";

function LoginReactHookForm() {
  type FormData = {
    email: string;
    password: string;
  };

  type LoginDataType = {
    employee_number: string;
    password: string;
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    // ログインボタンを押した時のみバリデーションを行う
    reValidateMode: "onSubmit",
  });

  const onSubmit = async (data: LoginDataType) => {
    const apiUrl = "http://localhost/back/api/login/";
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
    });

    if (response.ok) {
      // ログイン成功
      console.log("ログイン成功");
      router.push("/customers");
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
      <h1 className="flex flex-col items-center my-[10px] text-3xl text-gray-900">
        練習用アプリ
      </h1>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col items-center"
      >
        <div>
          <TextField
            className="w-[400px] my-[10px]"
            id="employee_number"
            name="employee_number"
            placeholder="社員番号"
            {...register("employee_number", {
              required: {
                value: true,
                message: "社員番号を入力してください",
              },
              pattern: {
                value: /^[0-9]{8}$/,
                message: "8桁の数字のみ入力してください。",
              },
            })}
          />
          {errors.employee_number?.message && (
            <div>{errors.employee_number.message}</div>
          )}
        </div>
        <div>
          <TextField
            className="w-[400px] my-[10px]"
            id="password"
            name="password"
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
          {errors.password?.message && <div>{errors.password.message}</div>}
        </div>
        <Button
          type="submit"
          size="large"
          variant="contained"
          color="primary"
          className="w-[400px] my-[10px]"
        >
          ログイン
        </Button>
      </form>
    </div>
  );
}

export default LoginReactHookForm;
