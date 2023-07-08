import React from 'react';
import Link from "next/link";
import { fetch_LOGIN } from '../features/utils/fetch';

const HelloWorld = () => {
  return (
    <>
      <h1>Login</h1>
      <div>
        <Link href="/"><h1 className='className="underline hover:no-underline text-gray-400 text-center text-sm my-3'>Homeへ</h1></Link>
      </div>
    </>
  );
};

export default HelloWorld;
