import Cookies from 'js-cookie';

type LoginProps = {
  url: string;
  body: string;
  resFunction: (data: any) => void;
};

export const baseUrl = process.env.NEXT_PUBLIC_RESTAPI_URL + '/api/';
export const credentials = 'include';

export const fetch_LOGIN = ({ url, body, resFunction }: LoginProps) => {
  const csrftoken = Cookies.get('csrftoken') || '';

  fetch(baseUrl + url, {
    method: 'POST',
    credentials: credentials,
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(body),
  })
    // このfetchは使用先ファイルにてレスポンスコード別対応を記述してるためステータスコード別のエラーハンドリング不要
    .then(resFunction)
    .catch((error) => {
      console.error(error);
    });
};
