import { HttpResponse, PathParams, http } from "msw";
import { BASE_URL } from "@/utils/fetch";
import { LoginDataType } from "@/components/forms/type";

export const AuthInfoHandlers = [
  http.post<PathParams, LoginDataType>(
    `${BASE_URL}/api/login/`,
    async ({ request }) => {
      const { employee_number, password } = await request.json();
      if (employee_number === "00000001" && password === "test") {
        return new HttpResponse(null, {
          status: 200,
        });
      } else {
        return new HttpResponse("社員番号またはパスワードが間違っています", {
          status: 400,
        });
      }
    },
  ),
];
