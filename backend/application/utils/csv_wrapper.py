"""CSV用のモジュール"""

import csv

from django.http import HttpResponse

from application.models import User


class CSVUserListData:
    """ユーザー一覧用のCSVデータクラス"""

    def __init__(self, users: list[User]):
        self.headers = [
            "社員番号",
            "名前",
            "メールアドレス",
            "権限",
        ]
        self.rows = self._create_rows(users)

        rows = []
        for user in users:
            rows.append(
                [
                    f'"{user.employee_number}"',
                    user.username,
                    user.employee_number,
                    user.role,
                ]
            )
        return rows


class CSVResponseWrapper:
    """csvのラッパークラス"""

    def __init__(self, filename: str):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        self.response = response

    def write_response(self, csv_data: CSVUserListData):
        """レスポンスにcsvを書き込む"""
        writer = csv.writer(self.response)
        writer.writerow(csv_data.headers)
        for row in csv_data.rows:
            writer.writerow(row)