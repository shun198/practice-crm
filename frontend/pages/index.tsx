import React from 'react';
import Link from "next/link";
import LoginForm from '../components/elements/Form/LoginForm';

const Login = () => {
  const submitHandler = (event) => {
    event.preventDefault();
  };

  return (
    <>
      <div>
        <LoginForm/>
        <Link href="/users"><h1>システムユーザ一覧</h1></Link>
      </div>
    </>
  );
}

export default Login;
