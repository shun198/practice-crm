import { useForm } from 'react-hook-form';

function LoginReactHookForm() {
  const { 
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    // ログインボタンを押した時のみバリデーションを行う
    reValidateMode: 'onSubmit',
  });

  const onSubmit = (data) => {
    console.log(data);
  }

  return (
    <div className="Login">
      <h1>ログイン</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <input
            id="employee_number"
            name="employee_number"
            placeholder="社員番号"
            {...register('employee_number', {
              required: {
                value: true, 
                message: '社員番号を入力してください',
              },
              pattern: {
                value: /^[0-9]{8}$/,
                message: '8桁の数字のみ入力してください。',
              },
            })} 
          />
            {errors.employee_number?.message && <div>{errors.employee_number.message}</div>}
        </div>
        <div>
          <input
            id="password"
            name="password"
            placeholder="パスワード"
            type="password"
            {...register('password', { 
              required: {
                value: true,
                message: 'パスワードを入力してください'
              },
              pattern: {
                value: /^(?=.*[a-zA-Z])(?=.*\d).{8,32}$/,
                message: '8文字以上、32文字以下の少なくとも1つ以上の半角英字と数字をもつパスワードを入力してください。',
              },
            })}
          />
            {errors.password?.message && <div>{errors.password.message}</div>}
        </div>
        <button type="submit">ログイン</button>
      </form>
    </div>
  );
}

export default LoginReactHookForm;