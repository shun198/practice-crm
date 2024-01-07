import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/router";

function VerifyUser() {
  const router = useRouter();
  const token: string | undefined = Array.isArray(router.query.token)
    ? router.query.token[0]
    : router.query.token;
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | undefined>();
  const [data, setData] = useState<any>({});
  const fetchCheckInvitationToken = async () => {
    try {
      const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/users/check_invitation_token`;
      const csrftoken = Cookies.get("csrftoken") || "";
      const credentials = "include";
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        credentials: credentials,
      });

      if (response.ok) {
        const responseData = await response.json();
        setData(responseData);
      } else {
        alert("エラーが発生しました");
      }
    } catch (error) {
      console.error("データの取得に失敗しました:", error);
    }
  };

  return isAuthenticated ? (
    <>
      <div title="初回パスワード設定">
        <h1>初回パスワード設定</h1>
      </div>
    </>
  ) : (
    <>
      <div title="トークン無効">
        <h1>初回パスワード設定</h1>
        <p className="whitespace-pre-line">{`有効期限が切れているかURLが間違っている可能性があるため、\n初回パスワード設定画面にアクセスできません。`}</p>
        <p>招待メールを再度送信してください。</p>
      </div>
    </>
  );
}

export default VerifyUser;
