import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import List from '@mui/material/List';
import ListSubheader from "@mui/material/ListSubheader";
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import SmartphoneIcon from '@mui/icons-material/Smartphone';
import EmailIcon from '@mui/icons-material/Email';
import CakeIcon from '@mui/icons-material/Cake';
import PersonIcon from '@mui/icons-material/Person';
import HomeIcon from '@mui/icons-material/Home';
import BadgeIcon from '@mui/icons-material/Badge';


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
        const apiUrl = `http://localhost/back/api/customers/${router.query.id}/`;
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
        } else if (response.status === 403) {
          setLoggedIn(false);
          router.push("/"); // ログインしていない場合にルートページにリダイレクト
        } else if (response.status === 404) {
          setLoggedIn(false);
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
      <List>        
        <ListSubheader component="div" id="nested-list-subheader">
            お客様詳細
        </ListSubheader>
        <ListItemIcon>
            <PersonIcon />
        </ListItemIcon>
        <ListItemText primary={data.name} />
        <ListItemText primary={data.kana} />
        <ListItemIcon>
            <CakeIcon />
        </ListItemIcon>
        <ListItemText primary={data.birthday} />
        <ListItemIcon>
            <EmailIcon />
        </ListItemIcon>
        <ListItemText primary={data.email} />
        <ListItemIcon>
            <SmartphoneIcon />
        </ListItemIcon>
        <ListItemText primary={data.phone_no} />
        <ListItemIcon>
            <HomeIcon />
        </ListItemIcon>
        <ListItemText primary={data.address} />
        <ListItemText primary={data.post_no} />
        <ListItemIcon>
            <BadgeIcon />
        </ListItemIcon>
        <ListItemText primary={data.updated_by} />
      </List>
    </div>
  );
}

export default CustomerDetail;
