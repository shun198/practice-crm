import React, { Dispatch, SetStateAction } from "react";
import { Button } from "@mui/material";
import router from "next/router";

export const ForgotPassword = () => {
  return (
    <div className="flex flex-row items-center h-20">
      <Button
        variant="text"
        className="text-16px text-link-blue"
        onClick={() => router.push("/password-reset")}
      >
        パスワードを忘れた方はこちら
      </Button>
    </div>
  );
};
