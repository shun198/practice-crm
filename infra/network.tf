# ------------------------------
# VPC Configuration
# ------------------------------
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # DNSによる名前解決をサポートする
  enable_dns_support = true
  # パブリックIPアドレスを持つインスタンスが対応するDNSホスト名を取得できるよう明示する
  enable_dns_hostnames = true

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-vpc" })
  )
}

# ------------------------------
# Internert Gateway Configuration
# ------------------------------
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-igw" })
  )
}

# ------------------------------
# Public Subnet Configuration
# ------------------------------
resource "aws_subnet" "public_a" {
  cidr_block = "10.0.1.0/24"
  # サブネットに配置されたインスタンスにパブリックIPアドレスが付与される
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${data.aws_region.current.name}a"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-a" })
  )
}

# ルートテーブルの設定
resource "aws_route_table" "public_a" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-a-rt" })
  )
}

# ルートテーブルをパブリックサブネットaと紐付ける
# タグをサポートしてないのでつけない
resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public_a.id
}

# IGWへのルーティングを設定
# タグをサポートしてないのでつけない
resource "aws_route" "public_internet_access_a" {
  route_table_id = aws_route_table.public_a.id
  # インターネット(0.0.0.0/0)へのアクセスを許可
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

# NATゲートウェイ用のElasticIPをpublic_a内に作成
resource "aws_eip" "public_a" {
  # EIPはVPC内に存在する
  vpc = true

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-a-eip" })
  )
}

# NATゲートウェイ
resource "aws_nat_gateway" "public_a" {
  # パブリックサブネットaに作成したElasticIPをNATに割り当てる(allocateする)
  allocation_id = aws_eip.public_a.id
  subnet_id     = aws_subnet.public_a.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-a-ngw" })
  )
}

resource "aws_subnet" "public_c" {
  cidr_block = "10.0.2.0/24"
  # サブネットに配置されたインスタンスにパブリックIPアドレスが付与される
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${data.aws_region.current.name}c"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-c" })
  )
}
resource "aws_route_table" "public_c" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-c-rt" })
  )
}

resource "aws_route_table_association" "public_c" {
  subnet_id      = aws_subnet.public_c.id
  route_table_id = aws_route_table.public_c.id
}

resource "aws_route" "public_internet_access_c" {
  route_table_id         = aws_route_table.public_c.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_eip" "public_c" {
  vpc = true

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-c-eip" })
  )
}

resource "aws_nat_gateway" "public_c" {
  allocation_id = aws_eip.public_c.id
  subnet_id     = aws_subnet.public_c.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public-c-ngw" })
  )
}
# ------------------------------
# Private Subnet Configuration
# ------------------------------
resource "aws_subnet" "private_a" {
  cidr_block        = "10.0.11.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "${data.aws_region.current.name}a"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private-a" })
  )
}

resource "aws_route_table" "private_a" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private-a-rt" })
  )
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private_a.id
}

resource "aws_route" "private_a_internet_out" {
  route_table_id = aws_route_table.private_a.id
  # インターネットへのアウトバウンドアクセスを可能にするためにNATの設定を行う
  nat_gateway_id         = aws_nat_gateway.public_a.id
  destination_cidr_block = "0.0.0.0/24"
}

resource "aws_subnet" "private_c" {
  cidr_block        = "10.0.12.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "${data.aws_region.current.name}c"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private-c" })
  )
}

resource "aws_route_table" "private_c" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private-c-rt" })
  )
}

resource "aws_route_table_association" "private_c" {
  subnet_id      = aws_subnet.private_c.id
  route_table_id = aws_route_table.private_c.id
}

resource "aws_route" "private_c_internet_out" {
  route_table_id = aws_route_table.private_c.id
  # インターネットへのアウトバウンドアクセスを可能にするためにNATの設定を行う
  nat_gateway_id         = aws_nat_gateway.public_c.id
  destination_cidr_block = "0.0.0.0/24"
}