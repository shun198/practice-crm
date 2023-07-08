import Cookies from 'js-cookie';
import router from 'next/router';
import { resStatusCheck } from '../constants/errorMessage';

type GetProps = {
  url: string;
  resCheck?: (res: Response) => void;
  resFunction?: (data: any) => void;
};

type LoginProps = {
  url: string;
  body: string;
  resFunction: (data: any) => void;
};

export const baseUrl = process.env.NEXT_PUBLIC_RESTAPI_URL + '/api/';
export const credentials = 'include';

// https://developer.mozilla.org/ja/docs/Web/API/fetch
export const fetch_GET = ({ url, resFunction }: GetProps) => {
  const csrftoken = Cookies.get('csrftoken') || '';
  fetch(baseUrl + url, {
    method: 'GET',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    credentials: credentials,
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else {
        if (res.status === 404) {
          router.push('/404');
        } else if (res.status === 403) {
          router.push('/');
        } else {
          resStatusCheck(res.status);
        }
      }
    })
    .then(resFunction)
    .catch((error) => {
      console.error(error);
    });
};

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
