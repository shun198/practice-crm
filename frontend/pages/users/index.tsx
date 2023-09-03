import React from 'react';
import Link from "next/link";


const UserList = () => {
  return (
    <>
      <h1>システムユーザ一覧</h1>
      <nav>
        <ul>
          <li>
            <Link href="/">ナビゲーション1</Link>
          </li>
          <li>
            <Link href="/">ナビゲーション2</Link>
          </li>
          <li>
            <Link href="/">ナビゲーション3</Link>
          </li>
        </ul>
      </nav>
      <div>
        <Link href="/"><h1>Homeへ</h1></Link>
      </div>
    </>
  );
};

export default UserList;