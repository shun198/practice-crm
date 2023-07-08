import { useRef, useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { FormValues } from '../types/FormTypes';
import { resStatusCheck } from '../constants/errorMessage';
import { fetch_LOGIN } from '../utils/fetch';

export const useLogin = () => {
  const router = useRouter();
  const { setError } = useForm<Partial<FormValues>>();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [isErrorFlag, setIsErrorFlag] = useState<boolean>(false);

  //エラーになったら、disabledを無効するように
  const resetRef = () => {
    if (buttonRef.current) {
      buttonRef.current.disabled = false;
    }
  };

  const logIn = (data: Partial<FormValues>) => {
    fetch_LOGIN({
      url: 'login/',
      body: data,
      resFunction: (res: Response) => {
        if (res.ok) {
          router.push('/users');
        } else {
          if (res.status === 400) {
            // id or passwordが間違っているとき
            setIsErrorFlag(true);
            setError('password', { type: 'custom' });
            resetRef();
          } else {
            resStatusCheck(res.status);
          }
        }
      },
    });
  };
  return { logIn, isErrorFlag };
};