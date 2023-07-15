import React from 'react';
import Link from "next/link";
import { useLogin } from '../features/users/useLogin';

const Login = () => {
  const { logIn, isErrorFlag } = useLogin();

  return (
    <>
      <h1>Login</h1>
      <div>
        <h1>ログイン画面</h1>
        {isErrorFlag && <p className="text-[#d32f2f]">パスワードか社員番号が間違っています</p>}
        <form method="post">
          <input type="text" id="employee_number" name="name" placeholder='社員番号'></input>
          <br/>
          <input type="text" id="password" name="name" placeholder='パスワード'></input>
          <br/>
          <button className="login_btn" type="submit">ログイン</button>
        </form>
        <Link href="/users"><h1>システムユーザ一覧</h1></Link>
      </div>
    </>
  );
}

export default Login;
