import { useState } from "react";

function LoginForm() {
  const [employeeNumber, setEmployeeNumber] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    // Prevent the browser from reloading the page
    // デフォルトでは、ブラウザはフォームデータを現在の URL に送信し、ページを更新します
    // e.preventDefault() を呼び出すことで、その振る舞いをオーバーライドできます
    e.preventDefault();
    // 次の課題としてここにFetchAPIでログイン機能を実装したい
    console.log({
      employeeNumber,
      password
    });
  };

  const handleChangeEmployeeNumber = (e) => {
    setEmployeeNumber(e.target.value);
  };
  const handleChangePassword = (e) => {
    setPassword(e.target.value);
  };

  return (
    <div>
      <h1>ログイン画面</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            id="employee_number"
            name="employee_number"
            placeholder="社員番号"
            type="text"
            onChange={handleChangeEmployeeNumber}
          />
        </div>
        <div>
          <input
            id="password"
            name="password"
            placeholder="パスワード"
            type="password"
            onChange={handleChangePassword}
          />
        </div>
        <div>
          <button type="submit">ログイン</button>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;
