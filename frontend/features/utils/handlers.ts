//enterキー押した後もsubmitしないように
export const checkKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') e.preventDefault();
  };