export type ApiType = {
    count: number;
    next: string;
    previous: string;
    results:
        | UserListValue[]
};

export type ApiResponse<T> = {
    count: number;
    next: string;
    previous: string;
    results: T;
};

export type UserListValue = {
    id: string;
    role: string;
    employee_number: string;
    name: string;
    email: string;
    verified: boolean;
    is_active: boolean;
};