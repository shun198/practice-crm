import React from "react";
import Link from "next/link";

const Header = () => {
    return (
        <nav>
        <ul>
          <li>
            <Link href="/">ナビゲーション1</Link>
          </li>
          <li>
            <Link href="/">ナビゲーション2</Link>
          </li>
          <li>
            <Link href="/">ナビゲーション3</Link>
          </li>
        </ul>
      </nav>
    )
}

export default Header