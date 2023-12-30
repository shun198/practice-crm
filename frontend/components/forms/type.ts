export type LoginDataType = {
  employee_number: string;
  password: string;
};

export type InviteUserType = {
  employee_number: string;
  username: string;
  email: string;
  role: BigInteger;
};
