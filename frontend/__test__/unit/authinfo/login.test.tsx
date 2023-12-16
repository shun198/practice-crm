// import { server } from '@/__test__/mocks/node';
// import { render, screen, waitFor, within } from '@testing-library/react';
// import LoginReactHookForm from '@/components/forms/LoginForm';

// describe('@/pages', () => {
//     test('login画面にログインボタン、社員番号、パスワード、パスワードリセットのボタンが期待通りに表示される', () => {
//         render(<LoginReactHookForm />);
//         expect(screen.getByRole('textbox', { name: '社員番号' })).toBeInTheDocument();
//         expect(screen.getByLabelText('パスワード')).toBeInTheDocument();
//         ['パスワードを忘れた方はこちら'].forEach((name) => {
//           expect(screen.getByRole('button', { name })).toBeInTheDocument();
//         });
//       });
// })


test('adds 1 + 2 to equal 3', () => {
  expect(1 + 2).toBe(3);
});