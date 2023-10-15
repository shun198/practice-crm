import Link from "next/link";


const LoginSuccess = () => {

  return (
    <>
      <h1>ログイン成功!</h1>
      <div>
        <Link href="/"><h1>Homeへ</h1></Link>
      </div>
    </>
  );
};

export default LoginSuccess;