export const ERROR_MESSAGES = {
  // form関連
  forms: {
    required: '必須項目です',
  },
} as const;

// ステータスコード受け取り時のエラーハンドリング関数
export const resStatusCheck = (statusCode: number) => {
  if (statusCode === 404) {
    alert('データが見つかりません。');
  } else if (statusCode === 500) {
    alert('通信エラーが発生しました。');
  } else if (statusCode === 504) {
    alert('タイムアウトエラーが発生しました。');
  } else {
    alert('エラーが発生し、処理に失敗しました。');
  }
};
