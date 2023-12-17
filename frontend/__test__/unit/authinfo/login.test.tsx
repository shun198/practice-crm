import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import mockRouter from "next-router-mock";
import LoginForm from "@/components/forms/LoginForm";

jest.mock("next/router", () => require("next-router-mock"));

describe("@/pages", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test("login画面にログインボタン、社員番号、パスワード、パスワード再設定のボタンが期待通りに表示される", () => {
    render(<LoginForm />);
    expect(screen.getByLabelText("社員番号")).toBeInTheDocument();
    expect(screen.getByLabelText("パスワード")).toBeInTheDocument();
    ["ログイン", "パスワードを忘れた方はこちら"].forEach((name) => {
      expect(screen.getByRole("button", { name })).toBeInTheDocument();
    });
  });

  test("パスワードと社員番号が空の時、ボタンを押下してたらエラーメッセージが表示される", async () => {
    render(<LoginForm />);
    await userEvent.click(screen.getByRole("button", { name: "ログイン" }));
    ["社員番号を入力してください", "パスワードを入力してください"].forEach(
      (name) => {
        expect(screen.getByText(name)).toBeInTheDocument();
      },
    );
  });

  test("パスワードが空、社員番号が7桁以下の時、ボタンを押下してたらエラーメッセージが表示される", async () => {
    render(<LoginForm />);
    await userEvent.type(screen.getByLabelText("社員番号"), "1234567");
    await userEvent.click(screen.getByRole("button", { name: "ログイン" }));
    ["8桁の数字のみ入力してください", "パスワードを入力してください"].forEach(
      (name) => {
        expect(screen.getByText(name)).toBeInTheDocument();
      },
    );
  });

  test("パスワードが空、社員番号が9桁以上の時、ボタンを押下してたらエラーメッセージが表示される", async () => {
    render(<LoginForm />);
    await userEvent.type(screen.getByLabelText("社員番号"), "123456789");
    await userEvent.click(screen.getByRole("button", { name: "ログイン" }));
    ["8桁の数字のみ入力してください", "パスワードを入力してください"].forEach(
      (name) => {
        expect(screen.getByText(name)).toBeInTheDocument();
      },
    );
  });

  //   test('パスワードと社員番号に適切な値(00000001,test)を入力した時、ボタンを押下するとお客様一覧画面へ遷移します', async () => {
  //     render(<LoginForm />);
  //     await userEvent.type(screen.getByLabelText('社員番号'), '00000001');
  //     await userEvent.tab();
  //     await userEvent.type(screen.getByLabelText('パスワード'), 'test');
  //     await userEvent.click(screen.getByRole('button', { name: 'ログイン' }));
  //     expect(mockRouter.asPath).toBe('/customers');
  //   });
});
