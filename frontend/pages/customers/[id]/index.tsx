import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import List from "@mui/material/List";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import SmartphoneIcon from "@mui/icons-material/Smartphone";
import EmailIcon from "@mui/icons-material/Email";
import CakeIcon from "@mui/icons-material/Cake";
import PersonIcon from "@mui/icons-material/Person";
import HomeIcon from "@mui/icons-material/Home";
import BadgeIcon from "@mui/icons-material/Badge";
import ListItem from "@mui/material/ListItem";
import SignpostIcon from "@mui/icons-material/Signpost";

type CustomerDetailData = {
  id: number;
  name: string;
  kana: string;
  birthday: Date;
  email: string;
  phone_no: string;
  address: string;
  post_no: string;
  updated_by: string;
};

function CustomerDetail() {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState<Boolean>(true);
  const [data, setData] = useState<any>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = `${process.env["NEXT_PUBLIC_API_URL"]}/api/customers/${router.query.id}`;
        const csrftoken = Cookies.get("csrftoken") || "";
        const credentials = "include";
        const response = await fetch(apiUrl, {
          method: "GET",
          headers: {
            "X-CSRFToken": csrftoken,
          },
          credentials: credentials,
        });

        if (response.ok) {
          const responseData: CustomerDetailData = await response.json();
          setData(responseData);
          setLoggedIn(true);
        } else if (response.status === 401 || 403) {
          setLoggedIn(false);
          router.push("/"); // ログインしていない場合にルートページにリダイレクト
        } else if (response.status === 404) {
          router.replace("/404"); // IDが存在しない場合は404ページへリダイレクト
        } else {
          alert("エラーが発生しました");
        }
      } catch (error) {
        console.error("データの取得に失敗しました:", error);
      }
    };

    if (router.isReady) {
      fetchData();
    }
  }, [router]);

  useEffect(() => {
    if (!loggedIn) {
      router.push("/");
    }
  }, [loggedIn]);

  if (!data) return null;

  return (
    <div className="customer-details">
      <h1 className="justify-center">お客様詳細</h1>
      <List>
        <ListItem disablePadding>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText>
            {data.name}({data.kana})
          </ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <CakeIcon />
          </ListItemIcon>
          <ListItemText>{data.birthday}</ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <EmailIcon />
          </ListItemIcon>
          <ListItemText>{data.email}</ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <SmartphoneIcon />
          </ListItemIcon>
          <ListItemText>{data.phone_no}</ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText>{data.address}</ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <SignpostIcon />
          </ListItemIcon>
          <ListItemText>{data.post_no}</ListItemText>
        </ListItem>
        <ListItem disablePadding>
          <ListItemIcon>
            <BadgeIcon />
          </ListItemIcon>
          <ListItemText>{data.updated_by}</ListItemText>
        </ListItem>
      </List>
    </div>
  );
}

export default CustomerDetail;
