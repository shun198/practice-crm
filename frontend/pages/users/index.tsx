import React from 'react';
import Link from "next/link";
import { fetch_GET } from '../../features/utils/fetch';
import { ApiResponse } from '../../features/types/ApiTypes';
import { UserListValue } from '../../features/types/ApiTypes';

const getUserList = (): Promise<ApiResponse<UserListValue[]>> => {
    return new Promise((resolve) => {
      fetch_GET({
        url: `users/`,
        resFunction: (data: ApiResponse<UserListValue[]>) => {
          resolve(data);
        },
      });
    });
  };


const UserList = () => {
  return (
    <>
      <h1>システムユーザ一覧</h1>
      <div>
        <Link href="/"><h1>Homeへ</h1></Link>
      </div>
    </>
  );
};

export default UserList;