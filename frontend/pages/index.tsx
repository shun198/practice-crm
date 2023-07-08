import React from 'react';
import Link from "next/link";
import { fetch_LOGIN } from '../features/utils/fetch';

const Login = () => {
  return (
    <>
      <h1>Login</h1>
      <div>
        <Link href="/users"><h1>システムユーザ一覧</h1></Link>
      </div>
    </>
  );
};

export default Login;
