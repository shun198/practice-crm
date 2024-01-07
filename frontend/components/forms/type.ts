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

export type CreateUserType = {
  customer: {
    name: string;
    kana: string;
    email: string;
    phone_no: string;
    birthday: string;
  };
  address: {
    prefecture: string;
    municipalities: string;
    house_no: string;
    other: string;
    post_no: string;
  };
};
